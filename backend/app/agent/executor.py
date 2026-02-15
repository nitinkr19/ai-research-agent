"""
Executor: runs research plans and produces findings.
Uses the LLM to execute each step and synthesize results.
"""

import asyncio
from app.agent.planner import create_plan
from app.tools.search import SearchTool
from app.llm.factory import get_llm_provider
from app.memory.faiss_store import FaissVectorStore


llm = get_llm_provider()
search_tool = SearchTool()
vector_store = FaissVectorStore(dim=3072)

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

    yield "🔎 Planning research...\n"
    await asyncio.sleep(0.01)

    plan = await asyncio.to_thread(create_plan, topic)

    yield "\n=== PLAN ===\n"
    for q in plan:
        yield f"- {q}\n"

    yield "\n🌐 Gathering research in parallel...\n\n"

    research_notes = []

    tasks = [fetch_question(q) for q in plan]
    research_notes = await asyncio.gather(*tasks)

    yield "📦 Chunking & indexing research...\n"

    # Store chunks
    for note in research_notes:
        vector_store.add(note)

    yield "🔎 Retrieving relevant context...\n"

    relevant_context = vector_store.search(topic, k=3)

    yield "\n🧠 Generating report...\n\n"

    messages = [
        {"role": "system", "content": "Write a structured report."},
        {"role": "user", "content": f"Topic: {topic}\n\nRelevant Context:\n{relevant_context}"}
    ]

    for chunk in llm.generate_stream(messages):
        yield chunk

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
