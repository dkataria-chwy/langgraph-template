"""
THIS FILE IS NEVER EDITED BY END-USERS.
It converts `config/workflow.yaml` into:
  • a dynamic State TypedDict
  • per-agent wrappers
  • a compiled LangGraph object

Public function:
    run_workflow(**initial_state_overrides)
"""

import importlib, asyncio, types, yaml
from typing import Annotated, List, Dict, TypedDict

from workflow_core.orchestrator_core import build_graph, default_state, Agent

# ── Load YAML spec ───────────────────────────────────────────────
with open("config/workflow.yaml", "r") as f:
    spec = yaml.safe_load(f)

agents_cfg: Dict[str, dict] = spec["agents"]
edges_cfg: Dict[str, List[str]] = spec["edges"]
entry_node: str = spec["entry"]
MAX_CC = spec.get("max_concurrency", 6)

# ── 1. build dynamic State TypedDict ─────────────────────────────
state_ns = {}
for agent in agents_cfg.values():
    for out_key in agent["outputs"]:
        # each key default type = object | None
        state_ns[out_key] = object

# create TypedDict subclass programmatically
State = types.new_class("State", (TypedDict,), dict(total=False))
State.__annotations__ = state_ns

# ── 2. generate wrappers  ────────────────────────────────────────
WRAPPERS: Dict[str, Agent] = {}

for name, cfg in agents_cfg.items():
    mod = importlib.import_module(cfg["module"])
    real_fn = getattr(mod, cfg["func"])
    outs: List[str] = cfg["outputs"]
    ins:  List[str] = cfg["inputs"]

    # build a thin async wrapper capturing cfg values
    async def wrapper(state, _fn=real_fn, _ins=ins, _outs=outs):
        # pull inputs from shared state in order
        args = [state[i] for i in _ins]
        result = await _fn(*args)
        # Wrap single return or tuple into dict keyed by outs
        if len(_outs) == 1:
            return {_outs[0]: result}
        else:
            return {k: v for k, v in zip(_outs, result)}

    wrapper.__name__ = f"{name}_wrapper"
    WRAPPERS[name] = wrapper

# ── 3. compile graph ─────────────────────────────────────────────
GRAPH = build_graph(
    state_model=State,
    agents=WRAPPERS,
    edges=edges_cfg,
    entry=entry_node,
    max_concurrency=MAX_CC,
)

# ── 4. helper for external callers (Dash / CLI / cron) ───────────
async def run_workflow(**initial):
    init_state = default_state(State, **initial)
    return await GRAPH.ainvoke(init_state) 