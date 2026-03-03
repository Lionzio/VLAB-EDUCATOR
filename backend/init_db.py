"""
Script de inicialização e "Seeding" do banco de dados.
Garante que as tabelas existam e que os dados mockados estejam disponíveis.
"""
import os
from flask import Flask
from dotenv import load_dotenv
from app.extensions import db
from app.models.database import StudentModel

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def seed_database():
    app = create_app()
    with app.app_context():
        # Cria as tabelas baseadas nos modelos ORM
        db.create_all()
        print("✅ Tabelas verificadas/criadas com sucesso no PostgreSQL.")

        # Verifica se o banco já tem alunos
        if StudentModel.query.first() is None:
            print("⏳ Populando alunos mockados...")
            students = [
                StudentModel(name="Ana", age=10, level="iniciante", learning_style="visual"),
                StudentModel(name="Carlos", age=15, level="intermediário", learning_style="cinestésico"),
                StudentModel(name="Mariana", age=22, level="avançado", learning_style="leitura-escrita")
            ]
            db.session.add_all(students)
            db.session.commit()
            print("✅ Alunos de teste inseridos no banco de dados!")
        else:
            print("✅ Banco de dados já possui registros de alunos.")

if __name__ == "__main__":
    seed_database()