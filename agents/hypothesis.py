"""
Hypothesis agent
Returns text or JSON.
"""

import asyncio

async def run(insights_md: str):
    await asyncio.sleep(1)
    return {"hypothesis": f"Hypothesis based on: {insights_md[:30]}..."} 