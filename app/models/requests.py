"""
Módulo responsável pelos DTOs (Data Transfer Objects) das requisições web.
"""

from pydantic import BaseModel, Field
from typing import Literal

class GenerateContentRequest(BaseModel):
    student_name: str = Field(..., description="Nome do aluno cadastrado no sistema (ex: Ana, Carlos, Mariana)")
    topic: str = Field(..., min_length=3, description="O tópico a ser ensinado (ex: Revolução Industrial)")
    content_type: Literal["conceitual", "pratico", "reflexao", "visual"] = Field(
        ..., description="O tipo de conteúdo que a LLM deve gerar"
    )