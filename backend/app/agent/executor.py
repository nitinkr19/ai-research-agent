"""
Executor: runs research plans and produces findings.
Uses the LLM to execute each step and synthesize results.
"""

import asyncio
from app.agent.planner import create_plan
from app.tools.search import SearchTool
from app.llm.factory import get_llm_provider
from app.memory.factory import get_vector_store
from app.memory.faiss_store import FaissVectorStore


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

    vector_store = get_vector_store()

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
    
    for note in research_notes:
        chunks = chunk_text(note)

        for chunk in chunks:
            vector_store.add(chunk)

    yield "🔎 Retrieving relevant context...\n"

    relevant_context = vector_store.search(topic, k=3)
    context_str = "\n\n".join(relevant_context)

    yield "\n🧠 Generating report...\n\n"

    messages = [
        {"role": "system", "content": "Write a concise structured report under 500 words."},
        {"role": "user", "content": f"Topic: {topic}\n\nRelevant Context:\n{context_str}"}
    ]

    max_chars = 4000
    count = 0

    for chunk in llm.generate_stream(messages):
        count += len(chunk)
        if count > max_chars:
            break
        yield chunk


async def fetch_question(question):
    return await search_tool.run(question)

def chunk_text(text, chunk_size=300):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks
