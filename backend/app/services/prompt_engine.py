"""
Motor de Engenharia de Prompt.
Isola a lógica de construção de texto das regras de negócio e infraestrutura.
"""
from app.models.database import StudentModel

class PromptEngine:
    def __init__(self):
        self.base_persona = (
            "Você é um Professor Universitário Sênior e Especialista em Design Instrucional. "
            "Seu objetivo é adaptar rigorosamente os conteúdos ao perfil psicológico e cognitivo do aluno."
        )

    def _build_context(self, student: StudentModel, topic: str) -> str:
        """Centraliza a injeção do contexto do aluno."""
        return (
            f"CONTEXTO DO ALUNO:\n"
            f"- Nome: {student.name}\n"
            f"- Idade: {student.age} anos\n"
            f"- Nível Cognitivo: {student.level}\n"
            f"- Estilo de Aprendizagem: {student.learning_style}\n\n"
            f"TÓPICO A SER ENSINADO: {topic}\n"
        )

    def _get_json_instruction(self, keys: str) -> str:
        """Garante que a LLM não alucine formatos fora do padrão."""
        return (
            "\n\nINSTRUÇÃO DE SAÍDA (STRICT JSON):\n"
            "Retorne APENAS um objeto JSON válido, sem crases, sem marcação markdown e sem textos adicionais.\n"
            f"O JSON DEVE conter EXATAMENTE as seguintes chaves: {keys}."
        )

    def generate_conceptual_prompt(self, student: StudentModel, topic: str) -> str:
        context = self._build_context(student, topic)
        instruction = "Crie uma explicação conceitual clara e didática sobre o tópico, ajustando o vocabulário à idade e ao nível do aluno."
        formatting = self._get_json_instruction('["raciocinio_didatico", "explicacao_conceitual"]')
        return f"{self.base_persona}\n\n{context}\n{instruction}{formatting}"

    def generate_practical_examples_prompt(self, student: StudentModel, topic: str) -> str:
        context = self._build_context(student, topic)
        instruction = "Crie 3 exemplos práticos e cotidianos que o aluno possa vivenciar na vida real para compreender o tópico."
        formatting = self._get_json_instruction('["raciocinio_didatico", "exemplos_praticos"]')
        return f"{self.base_persona}\n\n{context}\n{instruction}{formatting}"

    def generate_reflection_prompt(self, student: StudentModel, topic: str) -> str:
        context = self._build_context(student, topic)
        instruction = "Elabore 2 perguntas de reflexão profunda para estimular o pensamento crítico e socrático do aluno sobre o tópico."
        formatting = self._get_json_instruction('["raciocinio_didatico", "perguntas_reflexao"]')
        return f"{self.base_persona}\n\n{context}\n{instruction}{formatting}"

    def generate_visual_summary_prompt(self, student: StudentModel, topic: str) -> str:
        context = self._build_context(student, topic)
        instruction = "Crie um resumo estruturado. Se o estilo for 'visual', represente através de Arte ASCII. Se não, descreva um mapa mental detalhado."
        formatting = self._get_json_instruction('["raciocinio_didatico", "resumo_visual_ou_ascii"]')
        return f"{self.base_persona}\n\n{context}\n{instruction}{formatting}"