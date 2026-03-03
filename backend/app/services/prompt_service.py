"""
Service Layer: Orquestra Banco de Dados, PromptEngine e LLMClient.
Garante transações ACID no PostgreSQL.
"""
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.models.database import StudentModel, GeneratedContentModel
from app.extensions import db
from app.services.prompt_engine import PromptEngine
from app.services.llm_client import LLMClient

logger = logging.getLogger(__name__)

class PromptService:
    def __init__(self):
        self.engine = PromptEngine()
        self.llm = LLMClient() # Como é Singleton, pega a instância existente

    def generate(self, student_name: str, topic: str, content_type: str) -> dict:
        # 1. Busca aluno
        student = StudentModel.query.filter(StudentModel.name.ilike(student_name)).first()
        if not student:
            return {"erro": f"Aluno '{student_name}' não encontrado.", "status_code": 404}

        # 2. Caching (Query Otimizada)
        cached = GeneratedContentModel.query.filter_by(
            student_id=student.id, topic=topic, content_type=content_type
        ).first()

        if cached:
            logger.info(f"Cache Hit! Retornando '{topic}' do PostgreSQL.")
            return {
                "mensagem": "Conteúdo recuperado do cache.",
                "fonte": "banco_de_dados",
                "dados_gerados": cached.generated_data
            }

        # 3. Dispatch Dinâmico de Prompts (Mais limpo que vários IFs)
        prompt_methods = {
            "conceitual": self.engine.generate_conceptual_prompt,
            "pratico": self.engine.generate_practical_examples_prompt,
            "reflexao": self.engine.generate_reflection_prompt,
            "visual": self.engine.generate_visual_summary_prompt
        }

        generator = prompt_methods.get(content_type)
        if not generator:
             return {"erro": "Tipo de conteúdo inválido.", "status_code": 400}
             
        prompt = generator(student, topic)

        # 4. Requisição à IA
        llm_response = self.llm.generate_content(prompt)
        fonte = "mock_fallback" if "MOCK" in str(llm_response) else "api_gemini"

        # 5. Persistência com Transação Segura (Rollback)
        new_content = GeneratedContentModel(
            student_id=student.id,
            topic=topic,
            content_type=content_type,
            generated_data=llm_response
        )
        
        try:
            db.session.add(new_content)
            db.session.commit()
            logger.info(f"Novo conteúdo salvo no BD: {topic}")
        except SQLAlchemyError as e:
            db.session.rollback() # Desfaz alterações em caso de falha no banco
            logger.error(f"Erro ao salvar no banco: {e}")
            return {"erro": "Erro interno de persistência.", "status_code": 500}

        return {
            "mensagem": "Conteúdo gerado com sucesso!",
            "fonte": fonte,
            "dados_gerados": llm_response
        }