"""
Módulo de Modelos ORM (Object-Relational Mapping).
Mapeia as classes Python para tabelas reais no PostgreSQL.
"""
from datetime import datetime
from app.extensions import db

class StudentModel(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    level = db.Column(db.String(50), nullable=False)
    learning_style = db.Column(db.String(50), nullable=False)

    # Relacionamento: Um aluno pode ter vários conteúdos gerados
    contents = db.relationship('GeneratedContentModel', backref='student', lazy=True)

class GeneratedContentModel(db.Model):
    __tablename__ = 'generated_contents'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    content_type = db.Column(db.String(50), nullable=False)
    prompt_version = db.Column(db.String(20), default="v2.0")
    
    # O PostgreSQL possui suporte nativo maravilhoso para JSON!
    generated_data = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)