"""
Planner: breaks down research tasks into step-by-step plans.
Uses the LLM to generate structured research plans.
"""

from app.agent.prompts import PLANNING_SYSTEM, PLANNING_USER
from app.llm.base import BaseLLMProvider


class Planner:
    """Creates research plans from natural language tasks."""

    def __init__(self, llm: BaseLLMProvider):
        self.llm = llm

    async def create_plan(self, task: str) -> str:
        """
        Generate a research plan for the given task.

        Args:
            task: Natural language description of the research task.

        Returns:
            A step-by-step plan as a string.
        """
        messages = [
            {"role": "system", "content": PLANNING_SYSTEM},
            {"role": "user", "content": PLANNING_USER.format(task=task)},
        ]
        return await self.llm.complete(messages)
