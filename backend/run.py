"""
Ponto de entrada (Entrypoint).
Inicializa o Flask, Banco de Dados, Blueprints e permite CORS.
"""
import os
import logging
from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger  # <--- NOVA IMPORTAÇÃO
from dotenv import load_dotenv
from app.extensions import db
from app.api.routes import api_bp

load_dotenv()
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuração customizada do Swagger para ficar com a cara do V-Lab
    swagger_config = {
        "headers": [],
        "specs": [{"endpoint": 'apispec_1', "route": '/apispec_1.json', "rule_filter": lambda rule: True, "model_filter": lambda tag: True}],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"  # <--- Definimos a rota de volta para /docs!
    }
    
    # Inicia o Swagger
    Swagger(app, config=swagger_config, template={"info": {"title": "V-Lab Educator API", "version": "2.0"}})
    
    db.init_app(app)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"erro": "Rota não encontrada"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"erro": "Erro interno do servidor"}), 500
    
    @app.route('/')
    def health_check():
        return jsonify({"status": "online", "message": "V-Lab Educator Core Engine - Operacional"}), 200
        
    return app

if __name__ == '__main__':
    app = create_app()
    logger.info("Iniciando servidor V-Lab Educator...")
    app.run(host='0.0.0.0', port=5000, debug=True)