"""
Insight agent
Combines observation and interpretation markdown into insights.
"""

import asyncio

async def run(obs_md: str, interp_md: str) -> str:
    await asyncio.sleep(1)
    return f"# Insights\n\n{obs_md}\n\n{interp_md}" 