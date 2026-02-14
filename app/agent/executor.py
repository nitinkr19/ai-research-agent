"""
Executor: runs research plans and produces findings.
Uses the LLM to execute each step and synthesize results.
"""

from app.agent.prompts import EXECUTION_SYSTEM, EXECUTION_USER
from app.llm.base import BaseLLMProvider


class Executor:
    """Executes research plans and returns findings."""

    def __init__(self, llm: BaseLLMProvider):
        self.llm = llm

    async def execute(self, plan: str, task: str) -> str:
        """
        Execute a research plan for the given task.

        Args:
            plan: The step-by-step plan to follow.
            task: Original research task.

        Returns:
            The research findings as a string.
        """
        messages = [
            {"role": "system", "content": EXECUTION_SYSTEM},
            {"role": "user", "content": EXECUTION_USER.format(plan=plan, task=task)},
        ]
        return await self.llm.complete(messages)
