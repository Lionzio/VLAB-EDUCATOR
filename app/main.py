"""
Ponto de entrada (Entrypoint) da aplicação V-Lab Educator.
Configura o servidor FastAPI e anexa as rotas.
"""

from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="V-Lab Educator Platform",
    description="API para geração de conteúdo educativo personalizado via LLM.",
    version="1.0.0"
)

app.include_router(router, prefix="/api")

@app.get("/", summary="Health Check")
def root():
    """Rota raiz para verificar se a API está online."""
    return {"status": "online", "mensagem": "Bem-vindo ao V-Lab Educator API. Acesse /docs para a interface."}