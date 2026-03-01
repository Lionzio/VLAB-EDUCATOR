"""
Módulo responsável pelo acesso aos dados dos Alunos.
Implementa a leitura dos perfis salvos em formato JSON.
"""

import json
import os
from typing import List, Optional
from app.models.student import StudentProfile

class StudentRepository:
    def __init__(self, file_path: str = "data/students.json"):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            mock_students = [
                {"id": "1", "name": "Ana", "age": 10, "level": "iniciante", "learning_style": "visual"},
                {"id": "2", "name": "Carlos", "age": 15, "level": "intermediário", "learning_style": "cinestésico"},
                {"id": "3", "name": "Mariana", "age": 22, "level": "avançado", "learning_style": "leitura-escrita"}
            ]
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(mock_students, f, ensure_ascii=False, indent=4)

    def get_all_students(self) -> List[StudentProfile]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [StudentProfile(**student) for student in data]

    def get_student_by_name(self, name: str) -> Optional[StudentProfile]:
        students = self.get_all_students()
        for student in students:
            if student.name.lower() == name.lower():
                return student
        return None