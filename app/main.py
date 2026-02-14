"""
AI Research Agent - Main entry point.
Run the agent to perform autonomous AI research tasks.
"""

import asyncio
from app.core.config import settings
from app.llm.factory import get_llm_provider
from app.agent.planner import Planner
from app.agent.executor import Executor


async def main():
    """Run the AI research agent."""
    print("🤖 AI Research Agent starting...")

    # Initialize components
    llm = get_llm_provider()
    planner = Planner(llm=llm)
    executor = Executor(llm=llm)

    # Example: Plan and execute a simple research task
    task = "Explain the difference between supervised and unsupervised learning"
    print(f"\n📋 Task: {task}")

    plan = await planner.create_plan(task)
    print(f"\n📝 Plan: {plan}")

    result = await executor.execute(plan, task)
    print(f"\n✅ Result:\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
