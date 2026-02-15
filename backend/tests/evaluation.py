"""
Evaluation utilities for the research agent.
Run benchmarks and compare plan/response quality.
"""

import asyncio
from typing import List, Optional

# Add project root to path when running tests
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


async def evaluate_plan_quality(plan: str, task: str) -> float:
    """
    Simple heuristic for plan quality (0-1).
    Extend with LLM-as-judge or human eval for real metrics.
    """
    if not plan or not task:
        return 0.0
    # Basic checks: has multiple steps, mentions key concepts
    steps = [s.strip() for s in plan.split("\n") if s.strip() and s[0].isdigit()]
    score = min(1.0, len(steps) * 0.2) if steps else 0.2
    return round(score, 2)


async def run_eval_tasks(
    tasks: List[str],
    planner,
    executor,
) -> List[dict]:
    """Run evaluation on a list of tasks."""
    results = []
    for task in tasks:
        plan = await planner.create_plan(task)
        result = await executor.execute(plan, task)
        quality = await evaluate_plan_quality(plan, task)
        results.append({"task": task, "plan": plan, "result": result, "quality": quality})
    return results


# Example usage when run directly
if __name__ == "__main__":
    from app.llm.factory import get_llm_provider
    from app.agent.planner import Planner
    from app.agent.executor import Executor

    async def main():
        llm = get_llm_provider()
        planner = Planner(llm=llm)
        executor = Executor(llm=llm)
        tasks = ["What is reinforcement learning?"]
        results = await run_eval_tasks(tasks, planner, executor)
        for r in results:
            print(f"Task: {r['task']}\nQuality: {r['quality']}\n")

    asyncio.run(main())
