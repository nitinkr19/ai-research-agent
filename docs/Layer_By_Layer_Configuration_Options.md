## Layer-by-Layer Configuration Options

The AI Research Agent follows a modular layered architecture.  
Each layer can be independently configured and replaced.

---

## 1 Client Layer

Handles user interaction and external integration.

### Options

- **React Frontend**
  - Web-based interactive UI
  - Supports streaming responses
- **CLI**
  - Script-based research execution
  - Automation-friendly
- **REST API Consumers**
  - External system integration
- **Future: SDK (Python/JS)**
  - Embedded usage inside applications

---

## 2 API Layer

**Framework:** FastAPI  
Responsible for orchestration, routing, and streaming.

### Responsibilities

- Exposes REST endpoints
- Streams research responses (SSE)
- Routes requests to Planner & Executor
- Health monitoring

---

## 3 Agent Core Layer

Core reasoning and execution engine of the AI Research Agent.

### Components

#### 🧠 Planner
- Decomposes research topic into structured sub-questions
- Generates a step-by-step research plan
- Uses LLM for reasoning and task breakdown
- Supports iterative refinement

#### ⚙ Executor
- Executes planned research steps
- Calls search providers
- Collects and aggregates evidence
- Synthesizes structured research report
- Streams intermediate outputs (if enabled)

#### 🗂 Memory Manager
- Stores intermediate research results
- Enables contextual reuse across steps
- Interfaces with embedding & vector store layers
- Supports semantic retrieval

### Example Configuration

```bash
MAX_ITERATIONS=5
ENABLE_MEMORY=true
STREAM_RESULTS=true
```
---

## 4 LLM Layer

The LLM layer powers reasoning, planning, summarization, and final report generation.

### Responsibilities

- Task decomposition (used by Planner)
- Context-aware reasoning
- Evidence synthesis
- Report generation
- Iterative refinement

### Supported Providers

#### Local LLMs
- **Ollama**
  - llama2
  - mistral
  - custom local models
  - Fully offline capable

#### Cloud LLMs
- **OpenAI**
  - gpt-4
  - gpt-4o
  - gpt-3.5-turbo

- **Azure OpenAI**
  - Enterprise GPT deployments

- **Anthropic**
  - Claude models

#### Self-Hosted Models
- LLaMA variants
- Fine-tuned custom models

### Example Configuration

#### OpenAI

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o
```
OR
```bash
LLM_PROVIDER=ollama
OLLAMA_MODEL=mistral
OLLAMA_BASE_URL=http://localhost:11434
```
---

## 5 Search & Tools Layer

The Search & Tools layer retrieves external knowledge and supporting evidence.

### Responsibilities

- Perform search queries
- Retrieve relevant documents
- Extract structured and unstructured content
- Provide contextual evidence to the Executor
- Optionally perform deep content scraping

### Supported Providers

#### Web Search APIs
- **Tavily API**
- **Serper API** (Google wrapper)
- **Bing Search API**
- **Google Custom Search**

#### Academic & Research APIs
- **ArXiv API**
- **Semantic Scholar API**

#### Local / Development
- Local mock search (for testing)

#### Web Scraping
- HTML content extraction
- Full-page crawling
- Custom content parsers

### Example Configuration

```bash
SEARCH_PROVIDER=tavily
TAVILY_API_KEY=your_key
MAX_SEARCH_RESULTS=5
ENABLE_SCRAPING=true
```
---

## 6 Embedding Layer

The Embedding layer converts text into vector representations for semantic search and contextual retrieval.

### Responsibilities

- Transform documents into embeddings
- Enable similarity search
- Support semantic memory
- Power RAG-style retrieval workflows

### Supported Providers

#### Cloud Embeddings
- **OpenAI**
  - text-embedding-3-large
  - text-embedding-3-small

- **Cohere**
  - Commercial embedding APIs

#### Local Embeddings
- **Ollama**
  - nomic-embed-text
  - Other locally hosted embedding models

#### Open-Source
- **HuggingFace**
  - sentence-transformers
  - Custom embedding models

### Example Configuration

```bash
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-large
```
OR
```bash
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text
```
---

## 7 Vector Store Layer

The Vector Store layer stores embeddings and enables fast semantic similarity search.

### Responsibilities

- Store vector embeddings
- Perform nearest-neighbor similarity search
- Retrieve relevant contextual memory
- Support scalable semantic retrieval
- Enable RAG-style workflows

### Supported Vector Stores

#### Local

- **FAISS**
  - Lightweight
  - File-based storage
  - Fast local similarity search
  - Default option

#### Managed Cloud

- **Pinecone**
  - Fully managed vector database
  - Scalable and production-ready
  - Low operational overhead

#### Distributed / High-Scale

- **Milvus**
  - Distributed vector database
  - Suitable for large-scale deployments

- **Weaviate**
  - Hybrid graph + vector search
  - Supports metadata filtering

- **Qdrant**
  - High-performance vector search engine
  - Cloud and self-hosted options

### Example Configuration

#### FAISS (Local)

```bash
VECTOR_STORE=faiss
FAISS_INDEX_PATH=./data/index
```
OR
```bash
VECTOR_STORE=pinecone
PINECONE_API_KEY=your_key
PINECONE_INDEX=research-agent
```