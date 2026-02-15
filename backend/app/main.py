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

from fastapi import FastAPI
from app.llm.factory import get_llm_provider

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
        from app.agent.executor import run_agent_stream

        async for chunk in run_agent_stream(topic):
            safe_chunk = chunk.replace("\n", "\ndata: ")
            yield f"data: {safe_chunk}\n\n"

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