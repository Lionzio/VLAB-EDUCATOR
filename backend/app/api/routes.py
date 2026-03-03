"""
Roteador Web (Controller).
Interage apenas com a camada HTTP e delega as regras de negócio para a Service Layer.
Integração com Flasgger para documentação automática via Swagger UI.
"""
import logging
from flask import Blueprint, request, jsonify
from app.services.prompt_service import PromptService
from app.models.database import StudentModel

# Configuração de logger específico para a camada de rotas
logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__)
service = PromptService()

@api_bp.route('/students', methods=['GET'])
def list_students():
    """
    Lista todos os alunos cadastrados no sistema.
    ---
    tags:
      - Alunos
    responses:
      200:
        description: Retorna uma lista de alunos mockados.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "Ana"
              age:
                type: integer
                example: 10
              level:
                type: string
                example: "iniciante"
              learning_style:
                type: string
                example: "visual"
      500:
        description: Erro interno ao acessar o banco de dados.
    """
    try:
        students = StudentModel.query.all()
        result = [
            {
                "id": s.id, 
                "name": s.name, 
                "age": s.age, 
                "level": s.level, 
                "learning_style": s.learning_style
            } 
            for s in students
        ]
        return jsonify(result), 200
    except Exception as e:
        # Registramos o erro real no console para debug, mas retornamos uma mensagem amigável
        logger.error(f"Erro no banco de dados ao buscar alunos: {e}")
        return jsonify({"erro": "Não foi possível listar os alunos no momento."}), 500

@api_bp.route('/generate', methods=['POST'])
def generate_content():
    """
    Gera conteúdo educacional personalizado com IA.
    ---
    tags:
      - Geração de Conteúdo
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            student_name:
              type: string
              example: "Ana"
            topic:
              type: string
              example: "Revolução Francesa"
            content_type:
              type: string
              example: "conceitual"
    responses:
      201:
        description: Conteúdo gerado e salvo com sucesso.
      400:
        description: Erro de validação dos dados de entrada.
      404:
        description: Aluno não encontrado no banco de dados.
      415:
        description: Tipo de mídia não suportado (Falta de Content-Type JSON).
      500:
        description: Erro interno do servidor.
    """
    # 1. Validação de Segurança HTTP: Garante que a requisição seja um JSON
    if not request.is_json:
        return jsonify({"erro": "A requisição deve possuir o cabeçalho 'Content-Type: application/json'"}), 415

    data = request.get_json()
    
    # 2. Validação de Existência dos Campos
    required_fields = ["student_name", "topic", "content_type"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"erro": f"O corpo da requisição deve conter os campos obrigatórios: {required_fields}"}), 400

    student_name = data.get('student_name')
    topic = data.get('topic')
    content_type = data.get('content_type')

    # 3. Validação de Tipagem Defensiva (Evita crash no uso do método .strip())
    if not isinstance(student_name, str) or not isinstance(topic, str) or not isinstance(content_type, str):
        return jsonify({"erro": "Os campos 'student_name', 'topic' e 'content_type' devem ser textos."}), 400

    # 4. Delegação para a Service Layer
    try:
        response = service.generate(
            student_name=student_name.strip(),
            topic=topic.strip(),
            content_type=content_type.strip().lower()
        )

        if "erro" in response:
            status = response.pop("status_code", 400)
            return jsonify(response), status

        return jsonify(response), 201  # HTTP 201: Recurso Criado com Sucesso

    except Exception as e:
        logger.error(f"Erro não tratado na rota /generate: {e}")
        return jsonify({"erro": "Ocorreu um erro interno durante a geração do conteúdo."}), 500