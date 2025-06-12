"""
Interpretation agent
Returns Markdown text – LangGraph doesn't care about format.
Replace the body with your real OpenAI / API logic.
"""

import asyncio

async def run(customer_id: str) -> str:
    await asyncio.sleep(1)
    return f"# Interpretation for {customer_id}\n\n* Interpretation 1\n* Interpretation 2" 