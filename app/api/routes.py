"""
Módulo de rotas (Endpoints) da API.
Orquestra a comunicação entre os Repositórios (Dados) e os Serviços (IA).
"""

from fastapi import APIRouter, HTTPException
from app.models.requests import GenerateContentRequest
from app.repositories.student_repository import StudentRepository
from app.repositories.content_repository import ContentRepository
from app.services.prompt_engine import PromptEngine
from app.services.llm_client import LLMClient

router = APIRouter()

student_repo = StudentRepository()
content_repo = ContentRepository()
prompt_engine = PromptEngine()
llm_client = LLMClient()

@router.get("/students", summary="Listar Alunos")
def list_students():
    """Retorna todos os perfis de alunos disponíveis no sistema."""
    return student_repo.get_all_students()

@router.post("/generate", summary="Gerar Conteúdo Educativo")
def generate_content(request: GenerateContentRequest):
    """
    Gera um material didático personalizado usando IA.
    Seleciona o aluno, monta o prompt adequado, chama a LLM e salva o histórico.
    """
    student = student_repo.get_student_by_name(request.student_name)
    if not student:
        raise HTTPException(status_code=404, detail=f"Aluno '{request.student_name}' não encontrado.")

    prompt = ""
    if request.content_type == "conceitual":
        prompt = prompt_engine.generate_conceptual_prompt(student, request.topic)
    elif request.content_type == "pratico":
        prompt = prompt_engine.generate_practical_examples_prompt(student, request.topic)
    elif request.content_type == "reflexao":
        prompt = prompt_engine.generate_reflection_prompt(student, request.topic)
    elif request.content_type == "visual":
        prompt = prompt_engine.generate_visual_summary_prompt(student, request.topic)

    llm_response = llm_client.generate_content(prompt)
    
    # Tratamento de erro suave (Graceful Degradation)
    if "erro" in llm_response:
        raise HTTPException(status_code=503, detail=llm_response["erro"])

    file_path = content_repo.save_generated_content(
        student_name=student.name,
        topic=request.topic,
        content_type=request.content_type,
        llm_response=llm_response
    )

    return {
        "mensagem": "Conteúdo gerado e salvo com sucesso!",
        "arquivo_salvo": file_path,
        "dados_gerados": llm_response
    }