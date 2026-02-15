"""
AI Research Agent - Main entry point.
Run the agent to perform autonomous AI research tasks.
"""

import asyncio
from app.core.config import settings
from app.llm.factory import get_llm_provider
from app.agent.planner import create_plan
from app.agent.executor import Executor

from fastapi import FastAPI
from app.llm.factory import get_llm_provider

app = FastAPI()

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