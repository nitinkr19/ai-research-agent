"""
AI Research Agent - Main entry point.
Run the agent to perform autonomous AI research tasks.
"""

import asyncio
from app.core.config import settings
from app.llm.factory import get_llm_provider
from app.agent.planner import create_plan
from app.agent.executor import run_agent
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import sys

from fastapi import FastAPI
from app.llm.factory import get_llm_provider

from datetime import datetime
from fastapi import HTTPException

import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)

DAILY_LIMIT = 200
DAILY_LIMIT_PER_IP = 20

request_counts = defaultdict(int)
current_day = datetime.utcnow().date()

def check_daily_limit(request: Request):
    global current_day, request_counts

    today = datetime.utcnow().date()

    if today != current_day:
        current_day = today
        request_counts = defaultdict(int)
        request_count = 0

    client_ip = request.client.host

    if request_count >= DAILY_LIMIT:
        raise HTTPException(status_code=429, detail="Daily limit reached")

    if request_counts[client_ip] >= DAILY_LIMIT_PER_IP:
        raise HTTPException(
            status_code=429,
            detail="Daily limit per IP reached"
        )

    request_counts[client_ip] += 1
    request_count += 1

ENV = os.getenv("ENV", "dev")

if ENV == "prod":
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
else:
    app = FastAPI()

if ENV == "prod":
    allowed_origins = [
        "https://intelligentsearch.in",
        "https://www.intelligentsearch.in",
    ]
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = get_llm_provider()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/test")
def test_llm(prompt: str):
    messages = [
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": prompt}
    ]

    response = llm.generate(messages)
    return {"response": response}

@app.post("/plan")
def plan(topic: str):
    return {"questions": create_plan(topic)}

@app.post("/research")
def research(topic: str):
    return run_agent(topic)

@app.get("/research-stream")
async def research_stream(topic: str):
    async def generator():
        check_daily_limit()
        from app.agent.executor import run_agent_stream

        try:
            async for chunk in run_agent_stream(topic):
                safe_chunk = chunk.replace("\n", "\ndata: ")
                yield f"data: {safe_chunk}\n\n"
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield "\n\n❌ Internal error. Please try again later.\n"

    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.get("/test-stream")
async def test_stream():

    async def generator():
        for i in range(5):
            yield f"data: Hello {i}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(
        generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )

# async def main():
#     """Run the AI research agent."""
#     print("🤖 AI Research Agent starting...")

#     # Initialize components
#     llm = get_llm_provider()
#     planner = Planner(llm=llm)
#     executor = Executor(llm=llm)

#     # Example: Plan and execute a simple research task
#     task = "Explain the difference between supervised and unsupervised learning"
#     print(f"\n📋 Task: {task}")

#     plan = await planner.create_plan(task)
#     print(f"\n📝 Plan: {plan}")

#     result = await executor.execute(plan, task)
#     print(f"\n✅ Result:\n{result}")


# if __name__ == "__main__":
#     asyncio.run(main())