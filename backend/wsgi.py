"""
Ponto de Entrada WSGI (Web Server Gateway Interface) para Produção.
Este arquivo é o "maestro" que servidores como o Gunicorn (no Render) utilizam
para servir a aplicação Flask de forma escalável e segura.
"""
import os
import sys
import logging
from run import create_app

# Configuração de logging estruturado para capturarmos os logs na nuvem (Render)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [WSGI] - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

try:
    logger.info("Inicializando a aplicação Flask via WSGI (Produção)...")
    
    # Instancia a aplicação utilizando o padrão Factory definido no run.py
    app = create_app()
    
    logger.info("Aplicação instanciada com sucesso. Pronta para receber tráfego.")

except Exception as e:
    # Se faltar alguma variável de ambiente no Render (ex: DATABASE_URL),
    # o sistema avisa claramente no log em vez de simplesmente "apagar" o servidor.
    logger.critical(f"Falha crítica durante o boot da aplicação: {e}")
    sys.exit(1) # Força a parada caso a infraestrutura não esteja saudável

# ==============================================================================
# IMPORTANTE: O bloco abaixo só roda se você digitar "python wsgi.py". 
# Em produção, o Gunicorn ignora este bloco e lê apenas a variável "app" acima.
# ==============================================================================
if __name__ == "__main__":
    logger.warning("Aviso: Servidor de desenvolvimento iniciado via wsgi.py.")
    logger.warning("Para ambiente corporativo real, utilize o comando: gunicorn wsgi:app")
    
    # Plataformas de nuvem injetam a porta dinamicamente na variável de ambiente PORT.
    # O fallback (5000) garante que ainda rode localmente se necessário.
    porta_nuvem = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=porta_nuvem)