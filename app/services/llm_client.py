import os
import json
import requests
from functools import lru_cache
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY", "").strip()
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"
        self.headers = {"Content-Type": "application/json"}

    @lru_cache(maxsize=50)
    def generate_content(self, prompt: str) -> Dict[str, Any]:
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7, "responseMimeType": "application/json"}
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=10)
            
            # Se o Google der erro de limite (429), caímos no Mock para não travar o teste
            if response.status_code == 429:
                print("⚠️ Cota do Gemini excedida. Ativando Resposta Simulada (Mock) para teste...")
                return self._get_mock_response(prompt)
                
            response.raise_for_status() 
            result_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(result_text)
            
        except Exception as e:
            print(f"⚠️ Erro na API: {e}. Usando modo simulado.")
            return self._get_mock_response(prompt)

    def _get_mock_response(self, prompt: str) -> Dict[str, Any]:
        """Gera uma resposta estática para permitir que o sistema salve os JSONs."""
        return {
            "raciocinio_didatico": "O serviço de IA está em modo de segurança (cota atingida). Esta é uma resposta de simulação para validar a persistência de dados.",
            "explicacao_conceitual": "Conteúdo gerado em modo simulado devido ao limite da API gratuita do Google.",
            "exemplos_praticos": ["Exemplo simulado 1", "Exemplo simulado 2"],
            "perguntas_reflexao": ["Pergunta 1?", "Pergunta 2?"],
            "resumo_visual_ou_ascii": " [ MOCK DIAGRAM ] "
        }