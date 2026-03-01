"""
Módulo responsável pela modelagem e validação dos dados do Aluno.
Utiliza Pydantic para garantir a integridade dos dados na entrada da API,
aplicando o conceito de Fail-Fast (falhar rápido se o dado for inválido).
"""

from pydantic import BaseModel, Field
from typing import Literal

class StudentProfile(BaseModel):
    """
    Representa o perfil de um aluno no sistema educativo.
    Esta classe valida rigorosamente as características que serão 
    injetadas no contexto da LLM (Context Setting).
    """
    
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=100, 
        description="Nome completo ou primeiro nome do aluno",
        examples=["João da Silva"]
    )
    
    age: int = Field(
        ..., 
        gt=0, 
        lt=120, 
        description="Idade cronológica do aluno em anos",
        examples=[14]
    )
    
    # O uso do Literal restringe os valores aceitos na API exclusivamente a estas strings.
    # Se o usuário enviar "expert" ou "basico", o Pydantic retorna um erro HTTP 422 automaticamente.
    level: Literal["iniciante", "intermediário", "avançado"] = Field(
        ..., 
        description="Nível de conhecimento prévio do aluno sobre o tópico"
    )
    
    learning_style: Literal["visual", "auditivo", "leitura-escrita", "cinestésico"] = Field(
        ..., 
        description="Estilo predominante de aprendizado do aluno para adaptar a didática"
    )

    # Dica de Arquitetura: Em Python 3.11+, o Pydantic v2 é extremamente otimizado (escrito em Rust).
    # Manter os descritores no Field ajudará muito caso você decida gerar uma 
    # documentação automática da sua API (Swagger/OpenAPI) com o FastAPI depois!