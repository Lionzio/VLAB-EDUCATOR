V-Lab Educator: A ponte entre a inteligência artificial e a educação personalizada 🎓
Bem-vindo ao V-Lab Educator! Este projeto é uma plataforma de backend que utiliza Inteligência Artificial Generativa para criar materiais didáticos sob medida.
🌟 O porquê deste projeto (A visão)
Na educação tradicional, muitas vezes um mesmo conteúdo é passado da mesma forma para todos os alunos. Mas e se o material pudesse se adaptar?
O V-Lab Educator foi criado para resolver isso. Ele entende quem é o aluno — sua idade, seu nível de conhecimento e como ele aprende melhor (se é vendo imagens, lendo ou praticando) — e pede para a IA (Google Gemini 2.0) "traduzir" o conhecimento para aquela realidade específica.
🛠️ Como foi construído? (A engenharia)
Para garantir que o projeto fosse profissional e fácil de manter, utilizei práticas de mercado conhecidas como Clean Architecture (Arquitetura Limpa). O código é dividido em "camadas":
Camada de modelos (Models): Onde definimos as regras de validação. Usamos o Pydantic para garantir que, se um dado entrar errado (como uma idade negativa), o sistema pare na hora e avise o erro (Fail-Fast).
Camada de repositórios (Repositories): Responsável por salvar e ler os dados. Em vez de um banco de dados complexo, usamos arquivos JSON, o que facilita muito a portabilidade e a correção.
Camada de serviços (Services): Aqui mora o "cérebro". O sistema decide qual o melhor comando (prompt) enviar para a IA e gerencia a comunicação com o Google.
Camada de API (Routes): A porta de entrada. Criada com FastAPI, ela gera automaticamente uma página web para testarmos o sistema sem precisar de código.
🛡️ Resiliência: O diferencial
Durante o desenvolvimento, percebi que APIs gratuitas podem falhar por limites de uso. Para o sistema nunca deixar o usuário na mão, implementei um Mecanismo de Mock (Simulação). Se a IA do Google estiver fora do ar ou ocupada, o sistema detecta o erro e entrega uma resposta simulada de alta qualidade, garantindo que o fluxo não seja interrompido.
🚀 Como executar o projeto
Você tem duas formas de rodar este projeto. Escolha a que for mais confortável para você:
1. Usando Docker (O jeito mais rápido e limpo 🐳)
Se você tem o Docker instalado, não precisa se preocupar com Python ou bibliotecas.
Certifique-se de que o arquivo .env está na raiz com sua chave da API.
No terminal, execute:
Bash
docker build -t vlab-educator .
docker run -p 8000:8000 --env-file .env vlab-educator


Acesse: http://localhost:8000/docs
2. Rodando localmente (Passo a passo)
Ambiente virtual: Crie e ative seu ambiente (ex: python -m venv venv).
Dependências: Instale os pacotes necessários:
Bash
pip install -r requirements.txt


Configuração: Renomeie o arquivo .env.example (se houver) para .env e insira sua chave do Google Gemini.
Execução:
Bash
uvicorn app.main:app --reload


Teste: Abra o navegador em http://127.0.0.1:8000/docs.
📁 O que você vai encontrar no repositório?
app/: Todo o código fonte organizado por responsabilidade.
data/: Onde os perfis de alunos e o histórico de gerações são salvos.
samples/: [Importante para o Avaliador] Exemplos reais de arquivos gerados pelo sistema para conferência rápida.
PROMPT_ENGINEERING_NOTES.md: Um documento detalhando as técnicas de engenharia de prompt utilizadas.
Dockerfile: Configuração para rodar o projeto em containers.

🤝 Contato e feedback
Este projeto foi desenvolvido com foco em qualidade técnica e empatia pedagógica. Se tiver qualquer dúvida sobre a arquitetura ou as decisões de design, sinta-se à vontade para entrar em contato!