🎓 V-Lab Educator: Inteligência Artificial Moldando a Educação Personalizada

Bem-vindo ao V-Lab Educator! Este projeto é uma solução Full-Stack (Frontend, Backend e Banco de Dados) que utiliza Inteligência Artificial Generativa para criar materiais didáticos estritamente adaptados ao perfil de cada aluno.

🌟 A Visão: Por que este projeto existe? (Para o público geral)

Na educação tradicional, a sala de aula costuma seguir o modelo "tamanho único": o mesmo texto, a mesma explicação e o mesmo formato para dezenas de alunos diferentes. Mas sabemos que um estudante de 10 anos altamente visual aprende de forma muito diferente de um universitário de 20 anos que prefere a leitura reflexiva.

O V-Lab Educator resolve esse abismo educacional. Ele funciona como um "tradutor pedagógico". O sistema cruza as características do aluno (idade, nível de conhecimento, estilo de aprendizagem) com o tópico a ser ensinado. Em seguida, orienta a IA (Google Gemini 2.0) a gerar uma explicação personalizada, exemplos práticos, perguntas de reflexão ou até resumos visuais desenhados para aquela mente específica.

🛠️ A Engenharia: Como foi construído? (Para especialistas)

Para garantir que o projeto fosse escalável, testável e aderente às rigorosas demandas da Engenharia de Software moderna, o sistema evoluiu de um MVP simples para uma arquitetura Monorepo, dividindo responsabilidades de forma clara:

1. Frontend: React + Vite (Atomic Design)

A interface de usuário foi construída visando performance e reutilização extrema.

Componentização Estrita: Utilizamos a metodologia de Atomic Design. A interface é quebrada em Átomos (Botões, Inputs), Moléculas (Cards de Alunos) e Organismos (Listas, Formulários). É terminantemente proibido o uso de dados hardcoded; todo componente é agnóstico e recebe dados via props.

Renderização Iterativa (DRY): Listagens não repetem código. Utilizamos laços de repetição funcionais (.map()) para instanciar componentes base dinamicamente.
UX Resiliente: Tratamento global de erros, estados de loading granulares e feedback visual claro evitam que o usuário fique "preso" em caso de falhas de rede.

2. Backend: Python + Flask (Service Layer Pattern)

O servidor foi desenhado sob os princípios da Arquitetura Limpa (Clean Architecture), isolando a lógica de negócio da infraestrutura web.
Roteamento Modular: Utilização de Blueprints para separar as rotas da API.

Service Layer: A regra de negócio não fica nas rotas. Uma camada de serviço orquestra a comunicação entre o Banco de Dados, o Motor de Prompts e a API Externa.
Documentação Viva: Integração com Flasgger para geração automática do Swagger UI, permitindo testes interativos diretamente pelo navegador.

3. Persistência: PostgreSQL + ORM

Abandonamos arquivos locais em prol de um banco de dados relacional robusto.
Utilização do SQLAlchemy para o mapeamento Objeto-Relacional (ORM), garantindo que as consultas ao banco sejam feitas orientadas a objetos e protegidas contra falhas transacionais (Rollback).

O banco atua como uma camada de Cache Persistente: se um conteúdo já foi gerado antes para um perfil idêntico, o sistema poupa tokens da IA e retorna a resposta instantaneamente do banco de dados.

🛡️ Engenharia de Resiliência e Fallback

O maior desafio ao integrar APIs externas gratuitas são os limites de taxa (Rate Limits - Erro 429). O V-Lab Educator foi blindado com:
Padrão Singleton: Garante uma única instância de conexão com a IA.

Exponential Backoff: Utilizando a biblioteca Tenacity, se o Google negar uma requisição por excesso de tráfego, o backend não quebra. Ele entra em uma espiral de espera progressiva (2s, 4s, 8s) e tenta novamente.

Graceful Degradation (Modo Mock): Se houver uma falha catastrófica no provedor de IA, o sistema intercepta o erro, aciona um modo de simulação (Mock), salva o histórico no banco de dados e devolve um Status HTTP 201 (Sucesso) para o frontend. O fluxo de dados nunca para.

📂 Estrutura do Monorepo
Plaintext
/vlab-educator
├── backend/                  # API Python (Flask)
│   ├── app/                  # Regras de Negócio (Models, Services, API)
│   ├── init_db.py            # Script de criação de tabelas e Seeding
│   └── run.py                # Ponto de entrada do servidor
├── frontend/                 # Aplicação React + Vite
│   └── src/
│       ├── components/       # Átomos, Moléculas e Organismos
│       └── services/         # Configuração do Axios para comunicação HTTP
├── samples/                  # Exemplos estáticos gerados pela IA (Avaliação)
└── docker-compose.yml        # Orquestração da infraestrutura (PostgreSQL)

🚀 Como Executar o Projeto
Siga o passo a passo abaixo para rodar o ecossistema completo localmente.
Pré-requisitos
Docker e Docker Compose instalados (para o Banco de Dados).
Python 3.10+ instalado.
Node.js 18+ instalado.

Passo 1: Configurar Variáveis de Ambiente
Na pasta backend/, crie um arquivo .env com as seguintes chaves:
Snippet de código
LLM_API_KEY=sua_chave_do_google_gemini_aqui
DATABASE_URL=postgresql://vlab_admin:vlab_password@localhost:5433/vlab_educator_db

Passo 2: Subir o Banco de Dados
Na raiz do projeto, abra o terminal e execute:
Bash
docker-compose up -d
Isso iniciará o PostgreSQL na porta 5433 da sua máquina.

Passo 3: Inicializar o Backend (Flask)
Abra um terminal, navegue até a pasta backend/ e execute:
Crie e ative um ambiente virtual: python -m venv .venv (opcional, mas recomendado).
Instale as dependências: pip install -r requirements.txt
Popule o banco de dados inicial: python init_db.py
Inicie a API: python run.py
👉 Acesse o Swagger interativo em: http://localhost:5000/docs

Passo 4: Inicializar o Frontend (React)
Abra um novo terminal, navegue até a pasta frontend/ e execute:
Instale as bibliotecas Javascript: npm install
Rode o servidor de desenvolvimento: npm run dev
👉 Acesse a aplicação visual em: http://localhost:5173 (ou a porta informada no terminal do Vite).

🤝 Contato e Feedback
Este projeto foi desenvolvido com foco em excelência arquitetural, padrões de mercado e empatia pedagógica. Se tiver qualquer dúvida sobre as decisões de design de software, sinta-se à vontade para entrar em contato!