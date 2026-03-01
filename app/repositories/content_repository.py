"""
Módulo responsável pela persistência dos conteúdos gerados pela LLM.
Salva os resultados em disco garantindo rastreabilidade e histórico.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any

class ContentRepository:
    """
    Repositório para armazenar o histórico de conteúdos gerados.
    """
    
    def __init__(self, storage_dir: str = "data/history"):
        self.storage_dir = storage_dir
        # Garante que a pasta data/history exista
        os.makedirs(self.storage_dir, exist_ok=True)

    def save_generated_content(
        self, 
        student_name: str, 
        topic: str, 
        content_type: str, 
        llm_response: Dict[str, Any], 
        prompt_version: str = "v1.0"
    ) -> str:
        """
        Salva o conteúdo gerado em um arquivo JSON.
        O nome do arquivo inclui o tipo de conteúdo e um timestamp UNIX para evitar colisões.
        """
        # Formata o timestamp atual no padrão ISO 8601
        timestamp = datetime.now().isoformat()
        safe_topic = "".join([c if c.isalnum() else "_" for c in topic]).strip("_")
        
        # Estrutura final exigida para análise comparativa
        document = {
            "metadata": {
                "timestamp": timestamp,
                "student": student_name,
                "topic": topic,
                "content_type": content_type,
                "prompt_version": prompt_version
            },
            "generated_data": llm_response
        }
        
        # Cria um nome de arquivo único (Ex: explicacao_conceitual_20260301T092105.json)
        # O timestamp no formato de string garante que os arquivos fiquem ordenados cronologicamente
        file_time = datetime.now().strftime("%Y%m%dT%H%M%S")
        filename = f"{content_type}_{safe_topic[:20]}_{file_time}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(document, f, ensure_ascii=False, indent=4)
            
        return filepath