"""
Planner: breaks down research tasks into step-by-step plans.
Uses the LLM to generate structured research plans.
"""

import json
from app.llm.base import BaseLLMProvider
from app.llm.factory import get_llm_provider

llm = get_llm_provider()

def create_plan(topic: str) -> list[str]:

    messages = [
        {
            "role": "system",
            "content": (
                "You are a research planner. "
                "Break into EXACTLY 3 research questions."
                "Return ONLY valid JSON in this format:\n"
                '{"questions": ["question1", "question2"]}'
            )
        },
        {
            "role": "user",
            "content": topic
        }
    ]

    response = llm.generate(messages)

    try:
        parsed = json.loads(response)
        return parsed["questions"]
    except Exception:
        # fallback in case model misbehaves
        return [response]

# class Planner:
#     """Creates research plans from natural language tasks."""

#     def __init__(self, llm: BaseLLMProvider):
#         self.llm = llm

#     async def create_plan(self, task: str) -> str:
#         """
#         Generate a research plan for the given task.

#         Args:
#             task: Natural language description of the research task.

#         Returns:
#             A step-by-step plan as a string.
#         """
#         messages = [
#             {"role": "system", "content": PLANNING_SYSTEM},
#             {"role": "user", "content": PLANNING_USER.format(task=task)},
#         ]
#         return await self.llm.complete(messages)

#     import json