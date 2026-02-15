"""
Executor: runs research plans and produces findings.
Uses the LLM to execute each step and synthesize results.
"""

import asyncio
from app.agent.planner import create_plan
from app.tools.search import SearchTool
from app.llm.factory import get_llm_provider


llm = get_llm_provider()
search_tool = SearchTool()

def run_agent(topic: str):

    plan = create_plan(topic)

    research_notes = []

    for question in plan:
        result = search_tool.run(question)
        research_notes.append(result)

    messages = [
        {
            "role": "system",
            "content": "You are a research analyst. Write a structured report with headings."
        },
        {
            "role": "user",
            "content": (
                f"Topic: {topic}\n\n"
                f"Research Notes:\n{research_notes}"
            )
        }
    ]

    final_report = llm.generate(messages)

    return {
        "plan": plan,
        "report": final_report
    }

async def run_agent_stream(topic: str):

    plan = create_plan(topic)

    yield f"\n=== PLAN ===\n{plan}\n\n"
    await asyncio.sleep(0.1)

    research_notes = []
    
    tasks = [fetch_question(q) for q in plan]
    research_notes = await asyncio.gather(*tasks)

    messages = [
        {"role": "system", "content": "Write a structured report."},
        {"role": "user", "content": f"Topic: {topic}\nNotes: {research_notes}"}
    ]

    final_report = llm.generate(messages)

    for char in final_report:
        yield char
        await asyncio.sleep(0.005)

async def fetch_question(question):
    return search_tool.run(question)

# class Executor:
#     """Executes research plans and returns findings."""

#     def __init__(self, llm: BaseLLMProvider):
#         self.llm = llm

#     async def execute(self, plan: str, task: str) -> str:
#         """
#         Execute a research plan for the given task.

#         Args:
#             plan: The step-by-step plan to follow.
#             task: Original research task.

#         Returns:
#             The research findings as a string.
#         """
#         messages = [
#             {"role": "system", "content": EXECUTION_SYSTEM},
#             {"role": "user", "content": EXECUTION_USER.format(plan=plan, task=task)},
#         ]
#         return await self.llm.complete(messages)
