"""
Módulo responsável pela Engenharia de Prompt (O 'Cérebro' da aplicação).
Isola a criação de prompts da comunicação externa, facilitando testes unitários.
"""

from app.models.student import StudentProfile
import json

class PromptEngine:
    """
    Motor de geração de prompts dinâmicos.
    Garante que a LLM sempre receba um contexto forte e retorne um JSON estruturado.
    """

    def __init__(self):
        # Técnica 1: Persona Prompting
        self.base_persona = (
            "Você é um professor universitário sênior, especialista em pedagogia "
            "e design instrucional. Seu objetivo é adaptar conteúdos complexos "
            "para diferentes perfis de alunos de forma engajadora e didática."
        )

    def _build_context(self, student: StudentProfile, topic: str) -> str:
        """
        Técnica 2: Context Setting.
        Injeta os dados validados do aluno para guiar a LLM.
        """
        return (
            f"PERFIL DO ALUNO:\n"
            f"- Nome: {student.name}\n"
            f"- Idade: {student.age} anos\n"
            f"- Nível de Conhecimento: {student.level}\n"
            f"- Estilo de Aprendizado Predominante: {student.learning_style}\n\n"
            f"TÓPICO DA AULA:\n{topic}"
        )

    def _get_json_instruction(self, expected_keys: str) -> str:
        """
        Técnica 4: Output Formatting.
        Força a LLM a retornar exclusivamente um JSON válido, evitando textos soltos.
        """
        return (
            "\n\nINSTRUÇÃO DE FORMATAÇÃO ESTRITA:\n"
            "Retorne APENAS um objeto JSON válido, sem blocos de código Markdown (```json) "
            "e sem nenhum texto adicional antes ou depois. "
            f"O JSON DEVE conter estritamente as seguintes chaves: {expected_keys}."
        )

    def generate_conceptual_prompt(self, student: StudentProfile, topic: str) -> str:
        """
        Gera o prompt para 'Explicação conceitual' usando Chain-of-Thought.
        Exemplo de uso: topic = "Obras de Darcy Ribeiro e o nacionalismo brasileiro".
        """
        context = self._build_context(student, topic)
        
        # Técnica 3: Chain-of-Thought
        instruction = (
            "Sua tarefa é criar uma explicação conceitual sobre o tópico.\n"
            "PASSO A PASSO (Chain-of-Thought):\n"
            "1. Analise como a idade e o nível do aluno afetam o vocabulário a ser usado.\n"
            "2. Adapte a explicação para o estilo de aprendizado dele.\n"
            "3. Escreva a explicação final.\n"
        )
        
        formatting = self._get_json_instruction('["raciocinio_didatico", "explicacao_conceitual"]')
        return f"{self.base_persona}\n\n{context}\n\n{instruction}{formatting}"

    def generate_practical_examples_prompt(self, student: StudentProfile, topic: str) -> str:
        """
        Gera o prompt para 'Exemplos práticos'.
        """
        context = self._build_context(student, topic)
        
        instruction = (
            "Sua tarefa é criar 3 exemplos práticos e cotidianos que ilustrem o tópico.\n"
            "Os exemplos devem ser estritamente contextualizados para a idade do aluno "
            "e alinhados ao seu nível de conhecimento.\n"
        )
        
        formatting = self._get_json_instruction('["raciocinio_didatico", "exemplos_praticos"]')
        return f"{self.base_persona}\n\n{context}\n\n{instruction}{formatting}"

    def generate_reflection_prompt(self, student: StudentProfile, topic: str) -> str:
        """
        Gera o prompt para 'Perguntas de reflexão'.
        """
        context = self._build_context(student, topic)
        
        instruction = (
            "Sua tarefa é criar 2 perguntas de reflexão profunda sobre o tópico.\n"
            "O objetivo é estimular o pensamento crítico do aluno, fazendo-o questionar "
            "o status quo ou analisar o assunto sob uma ótica diferente.\n"
        )
        
        formatting = self._get_json_instruction('["raciocinio_didatico", "perguntas_reflexao"]')
        return f"{self.base_persona}\n\n{context}\n\n{instruction}{formatting}"

    def generate_visual_summary_prompt(self, student: StudentProfile, topic: str) -> str:
        """
        Gera o prompt para 'Resumo visual'.
        """
        context = self._build_context(student, topic)
        
        instruction = (
            "Sua tarefa é criar um resumo visual do tópico.\n"
            "Se o aluno for do estilo 'visual', crie um diagrama usando arte ASCII.\n"
            "Para outros estilos, crie uma descrição textual vívida de um mapa mental.\n"
        )
        
        formatting = self._get_json_instruction('["raciocinio_didatico", "resumo_visual_ou_ascii"]')
        return f"{self.base_persona}\n\n{context}\n\n{instruction}{formatting}"