"""
Módulo de comunicação HTTP com a API da LLM (Google Gemini).
Padrões aplicados: Singleton, Retry com Exponential Backoff e Fallback.
"""

import os
import json
import logging
import requests
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv

load_dotenv()

# Logging profissional substitui os "prints" para facilitar auditoria em produção
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class RateLimitError(Exception):
    """Exceção customizada para identificar limite de cota do Google (429)."""
    pass

class LLMClient:
    """
    Implementação do Padrão Singleton.
    Garante que a aplicação use uma única instância de configuração e pool de conexões.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Construtor real executado apenas na primeira vez."""
        self.api_key = os.getenv("LLM_API_KEY", "").strip()
        if not self.api_key:
            logger.error("CRÍTICO: Chave LLM_API_KEY não encontrada no .env!")
            
        self.headers = {"Content-Type": "application/json"}
        self.primary_model = "gemini-2.0-flash"

    def _get_url(self, model: str) -> str:
        return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"

    # O Tenacity assume o controle: se der RateLimitError, ele espera e tenta de novo sozinho.
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=10), # Espera 2s, 4s, 8s...
        retry=retry_if_exception_type(RateLimitError),
        reraise=True
    )
    def _make_request(self, payload: dict) -> dict:
        url = self._get_url(self.primary_model)
        response = requests.post(url, headers=self.headers, json=payload, timeout=15)
        
        if response.status_code == 429:
            logger.warning("Cota excedida (429). O Tenacity acionará o Backoff Exponencial...")
            raise RateLimitError("Limite de requisições do Gemini atingido.")
            
        response.raise_for_status() # Levanta exceção para erros 400 ou 500 genéricos
        return response.json()

    def generate_content(self, prompt: str) -> Dict[str, Any]:
        """Orquestra a chamada e aplica o Fallback de Mock em caso de falha catastrófica."""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.7, "responseMimeType": "application/json"}
        }
        
        try:
            data = self._make_request(payload)
            result_text = data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(result_text)
            
        except json.JSONDecodeError:
            logger.error("O modelo não retornou um JSON válido.")
            return {"erro": "Erro de formatação na resposta da IA."}
        except Exception as e:
            logger.error(f"Falha total após retentativas ou erro de rede: {e}. Acionando Mock.")
            return self._get_mock_response()

    def _get_mock_response(self) -> Dict[str, Any]:
        """Degradação Graciosa: Mantém o sistema vivo se a IA cair."""
        return {
            "raciocinio_didatico": "[MOCK] A IA está indisponível. Acionando contingência.",
            "explicacao_conceitual": "Este é um conteúdo simulado para garantir a persistência dos dados e a resiliência do sistema.",
        }