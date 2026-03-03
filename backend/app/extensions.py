"""
Módulo responsável por instanciar as extensões do Flask.
Mantém a aplicação desacoplada e previne importações circulares.
"""
from flask_sqlalchemy import SQLAlchemy

# Instância global do SQLAlchemy (ORM)
db = SQLAlchemy()