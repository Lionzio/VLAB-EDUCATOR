"""
Módulo responsável pela comunicação HTTP com a API da LLM.
Implementa cache em memória e tratamento robusto de falhas (Graceful Degradation).
"""

import os
import json
import requests
from functools import lru_cache
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    """
    Cliente isolado para interagir com a API de Inteligência Artificial.
    """

    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        
        if not self.api_key:
            raise ValueError("ERRO CRÍTICO: Chave LLM_API_KEY não encontrada no arquivo .env")
            
        # Configuração para OpenAI REST API
        self.url = "[https://api.openai.com/v1/chat/completions](https://api.openai.com/v1/chat/completions)"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    # Implementação do requisito de Cache (evita chamadas redundantes e gastos de token)
    @lru_cache(maxsize=50)
    def _cached_request(self, prompt: str) -> Optional[Dict[str, Any]]:
        """
        Método interno em cache que faz a chamada HTTP real.
        O lru_cache garante que se a mesma string de prompt for enviada,
        a resposta salva na memória RAM será retornada instantaneamente.
        """
        payload = {
            "model": "gpt-4o-mini",  # Versão recomendada pelo edital (Free Tier/Low Cost)
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "response_format": {"type": "json_object"} # Força a API a respeitar o JSON
        }

        try:
            # Timeout de 15s para evitar que a aplicação trave se a API cair
            response = requests.post(self.url, headers=self.headers, json=payload, timeout=15)
            response.raise_for_status() # Levanta exceção se o HTTP Status não for 2xx
            
            result_text = response.json()["choices"][0]["message"]["content"]
            return json.loads(result_text)
            
        except requests.exceptions.Timeout:
            print("AVISO: A API da LLM demorou muito para responder (Timeout).")
            return {"erro": "Serviço temporariamente indisponível por lentidão."}
            
        except requests.exceptions.HTTPError as e:
            print(f"AVISO: Erro HTTP na API da LLM: {e}")
            return {"erro": "Falha na comunicação com o provedor de IA."}
            
        except json.JSONDecodeError:
            print("AVISO: A LLM não retornou um JSON válido.")
            return {"erro": "Erro de formatação na resposta da IA."}
            
        except Exception as e:
            print(f"ERRO DESCONHECIDO: {e}")
            return {"erro": "Ocorreu um erro interno inesperado."}

    def generate_content(self, prompt: str) -> Dict[str, Any]:
        """
        Método público que a aplicação consome.
        Repassa o prompt para o método com cache.
        """
        # Em arquiteturas reais, poderíamos ter uma lógica de fallback aqui.
        # Ex: Se falhar na OpenAI, tenta no Gemini.
        return self._cached_request(prompt)