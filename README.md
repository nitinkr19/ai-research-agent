# AI Research Agent

Learn AI by building an autonomous research agent. Enter a topic, and the agent plans research questions, gathers information, and generates a structured report—with optional streaming output to the UI.

## Architecture

- **Backend** (FastAPI): LLM-powered planner, executor, search tools (local + Tavily), vector store (FAISS), and REST + SSE endpoints
- **Frontend** (React): Simple UI to submit topics and stream research reports in real time

## Project Structure

```
ai-research-agent/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app & endpoints
│   │   ├── core/
│   │   │   └── config.py        # Settings from .env
│   │   ├── llm/
│   │   │   ├── base.py
│   │   │   ├── openai_provider.py
│   │   │   ├── ollama_provider.py
│   │   │   └── factory.py
│   │   ├── agent/
│   │   │   ├── planner.py       # Breaks topics into research questions
│   │   │   ├── executor.py     # Runs research & generates reports
│   │   │   └── prompts.py
│   │   ├── memory/
│   │   │   ├── base.py
│   │   │   ├── vector_store.py  # In-memory store
│   │   │   ├── faiss_store.py   # FAISS + Ollama embeddings
│   │   │   └── factory.py
│   │   └── tools/
│   │       ├── base.py
│   │       ├── search.py        # Local simulated search
│   │       ├── tavily_search.py # Tavily API search
│   │       └── factory.py
│   ├── tests/
│   │   ├── test_main.py
│   │   ├── test_config.py
│   │   ├── test_llm_*.py
│   │   ├── test_agent_*.py
│   │   ├── test_tools_*.py
│   │   ├── test_memory_*.py
│   │   └── evaluation.py
│   ├── .env
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── frontend/
│   ├── src/
│   │   └── App.js
│   └── package.json
│
├── CODEOWNERS              # PR reviewers (replace @your-github-username)
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── REQUIRE_REVIEW.md   # How to set branch protection
│   └── workflows/
│       └── test.yml        # CI runs pytest on PRs
└── README.md
```

## Prerequisites

- **Python 3.11+**
- **Node.js 18+** (for frontend)
- **Ollama** (for local LLMs + embeddings) or **OpenAI API key**
- **Tavily API key** (optional, for web search)

### Ollama (local models)

```bash
# Install: https://ollama.ai
ollama pull llama2
ollama pull nomic-embed-text   # for embeddings (if using FAISS)
```

```mermaid
flowchart TD
    %% CLIENT LAYER
    subgraph CLIENT
        UI[React Frontend]
        CLI[CLI / Scripts]
    end

    %% API LAYER
    subgraph API
        FastAPI[FastAPI Server]
    end

    %% AGENT CORE
    subgraph AGENT_CORE
        Planner[Planner]
        Executor[Executor]
        Memory[Memory Manager]
    end

    %% LLM LAYER
    subgraph LLM_LAYER
        LLM[LLM Provider]
    end

    %% SEARCH LAYER
    subgraph SEARCH_LAYER
        LocalSearch[Local Search]
        Tavily[Tavily API]
        <!-- ExternalSearch[External APIs]
        Scraper[Web Scraper] -->
    end

    %% EMBEDDING LAYER
    subgraph EMBEDDING_LAYER
        OpenAIEmb[OpenAI Embeddings]
        OllamaEmb[Ollama Embeddings]
        <!-- HFEmb[HuggingFace / Other] -->
    end

    %% VECTOR STORE
    subgraph VECTOR_STORE
        FAISS[FAISS]
        <!-- Pinecone[Pinecone]
        Milvus[Milvus]
        Weaviate[Weaviate]
        Qdrant[Qdrant] -->
    end

    %% FLOW
    UI --> FastAPI
    CLI --> FastAPI
    FastAPI --> Planner
    Planner --> LLM
    Planner --> Executor
    Executor --> LLM
    Executor --> SEARCH_LAYER
    SEARCH_LAYER --> Memory
    Memory --> EMBEDDING_LAYER
    EMBEDDING_LAYER --> VECTOR_STORE
    VECTOR_STORE --> Executor
    Executor --> FastAPI
    FastAPI --> UI
```

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # Edit if needed
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend

```bash
cd frontend
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000), enter a research topic, and click **Run Research**.

## Configuration

Create `backend/.env` (or copy from `.env.example`):

| Variable | Description |
|----------|-------------|
| `LLM_PROVIDER` | `ollama` or `openai` |
| `OLLAMA_BASE_URL` | Default: `http://localhost:11434` |
| `OLLAMA_MODEL` | e.g. `llama2`, `mistral` |
| `OPENAI_API_KEY` | Required when `LLM_PROVIDER=openai` |
| `OPENAI_MODEL` | e.g. `gpt-4`, `gpt-3.5-turbo` |
| `SEARCH_PROVIDER` | `local` or `tavily` |
| `TAVILY_API_KEY` | Required when `SEARCH_PROVIDER=tavily` |
| `VECTOR_STORE` | `faiss` (FAISS + Ollama embeddings) |
| `EMBEDDING_MODEL` | Ollama embedding model, e.g. `nomic-embed-text` |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/test` | Test LLM with a prompt (`?prompt=...`) |
| POST | `/plan` | Get research questions for a topic (`?topic=...`) |
| POST | `/research` | Run full research (returns plan + report) |
| GET | `/research-stream` | Stream research report via SSE (`?topic=...`) |

## Running Tests

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v
```

To run with coverage:

```bash
pytest -v --cov=app --cov-report=term-missing
```

Tests use mocks for external services (Ollama, OpenAI, Tavily) so no API keys or running services are required.

## Docker

```bash
cd backend
docker compose up --build
```

Backend runs on port 8000. For Ollama, use the host via `host.docker.internal:11434` (already configured in `docker-compose.yml`).

## Contributing

This is an open-source project. All pull requests require review and approval from the maintainers before merging. See [CODEOWNERS](CODEOWNERS) for reviewers. Please ensure tests pass before submitting a PR.

## Extending the Agent

- **Search**: Switch `SEARCH_PROVIDER=tavily` and set `TAVILY_API_KEY` for real web search.
- **Vector store**: FAISS with Ollama embeddings is used for semantic search over research chunks.
- **Prompts**: Edit `backend/app/agent/prompts.py` to tune planning and execution behavior.

## License

See [LICENSE](LICENSE).
