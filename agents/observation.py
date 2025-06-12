"""
Observation agent
Returns Markdown text – LangGraph doesn't care about format.
Replace the body with your real OpenAI / API logic.
"""

import asyncio

async def run(customer_id: str) -> str:
    await asyncio.sleep(1)  # simulate latency
    return f"# Observations for {customer_id}\n\n* Item 1\n* Item 2" 