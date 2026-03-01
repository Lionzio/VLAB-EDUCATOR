"""
Módulo responsável pela modelagem e validação dos dados do Aluno.
"""

from pydantic import BaseModel, Field
from typing import Literal

class StudentProfile(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nome completo ou primeiro nome do aluno")
    age: int = Field(..., gt=0, lt=120, description="Idade cronológica do aluno em anos")
    level: Literal["iniciante", "intermediário", "avançado"] = Field(
        ..., description="Nível de conhecimento prévio do aluno sobre o tópico"
    )
    learning_style: Literal["visual", "auditivo", "leitura-escrita", "cinestésico"] = Field(
        ..., description="Estilo predominante de aprendizado do aluno para adaptar a didática"
    )