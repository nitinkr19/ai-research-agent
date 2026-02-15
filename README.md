# AI Research Agent

Learn AI by building an autonomous research agent. Enter a topic, and the agent plans research questions, gathers information, and generates a structured report—with optional streaming output to the UI.

## Architecture

- **Backend** (FastAPI): LLM-powered planner, executor, search tools, and REST + SSE endpoints
- **Frontend** (React): Simple UI to submit topics and stream research reports in real time

## Project Structure

```
ai-research-agent/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app & endpoints
│   │   ├── core/
│   │   │   └── config.py     # Settings from .env
│   │   ├── llm/
│   │   │   ├── base.py
│   │   │   ├── openai_provider.py
│   │   │   ├── ollama_provider.py
│   │   │   └── factory.py
│   │   ├── agent/
│   │   │   ├── planner.py    # Breaks topics into research questions
│   │   │   ├── executor.py   # Runs research & generates reports
│   │   │   └── prompts.py
│   │   ├── memory/
│   │   │   └── vector_store.py
│   │   └── tools/
│   │       ├── search.py     # Search tool (extend for web search)
│   │       └── base.py
│   ├── tests/
│   │   └── evaluation.py
│   ├── .env
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── frontend/
│   ├── src/
│   │   └── App.js            # React UI with SSE streaming
│   └── package.json
│
└── README.md
```

## Prerequisites

- **Python 3.11+**
- **Node.js 18+** (for frontend)
- **Ollama** (for local LLMs) or **OpenAI API key**

### Ollama (local models)

```bash
# Install: https://ollama.ai
ollama pull llama2
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

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/test` | Test LLM with a prompt |
| POST | `/plan` | Get research questions for a topic |
| POST | `/research` | Run full research (returns plan + report) |
| GET | `/research-stream` | Stream research report via SSE |

## Docker

```bash
cd backend
docker compose up --build
```

Backend runs on port 8000. For Ollama, use the host via `host.docker.internal:11434` (already configured in `docker-compose.yml`).

## Extending the Agent

- **Search**: Replace the simulated search in `backend/app/tools/search.py` with SerpAPI, Tavily, or DuckDuckGo.
- **Vector store**: Use ChromaDB or FAISS in `backend/app/memory/vector_store.py` for semantic search.
- **Prompts**: Edit `backend/app/agent/prompts.py` to tune planning and execution behavior.

## License

See [LICENSE](LICENSE).
