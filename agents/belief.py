"""
Belief agent
Returns Markdown text – LangGraph doesn't care about format.
Replace the body with your real OpenAI / API logic.
"""

import asyncio

async def run(customer_id: str) -> str:
    await asyncio.sleep(1)
    return f"# Belief for {customer_id}\n\n* Belief 1\n* Belief 2" 