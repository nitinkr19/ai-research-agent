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
from collections import defaultdict
from fastapi import Request, HTTPException

import threading
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True,
)

# Limits
GLOBAL_DAILY_LIMIT = 200
PER_IP_DAILY_LIMIT = 20

# State
global_count = 0
ip_counts = defaultdict(int)
current_day = datetime.utcnow().date()

# Lock (important for concurrency safety)
lock = threading.Lock()


def check_daily_limits(request: Request):
    global global_count, ip_counts, current_day

    today = datetime.utcnow().date()

    with lock:
        # Reset counters if new day
        if today != current_day:
            current_day = today
            global_count = 0
            ip_counts = defaultdict(int)

        client_ip = request.client.host

        # Check global limit first
        if global_count >= GLOBAL_DAILY_LIMIT:
            raise HTTPException(
                status_code=429,
                detail="Global daily limit reached"
            )

        # Check per-IP limit
        if ip_counts[client_ip] >= PER_IP_DAILY_LIMIT:
            raise HTTPException(
                status_code=429,
                detail="Daily limit per IP reached"
            )

        # Increment counters
        global_count += 1
        ip_counts[client_ip] += 1

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
async def research_stream(request: Request, topic: str):
    async def generator():
        check_daily_limits(request)
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