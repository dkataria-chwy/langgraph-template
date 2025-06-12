# langgraph-workflow-template

A plug-and-play orchestration template for LangGraph AI agent workflows. This project lets you define, edit, and run complex agent DAGs (Directed Acyclic Graphs) **without touching Python code** after deployment. All workflow changes are made in a single YAML file.

## Features
- **No-code workflow editing:** All DAG changes (add/remove agents, change edges, I/O keys) are made in `config/workflow.yaml`.
- **Flexible agent outputs:** Agents can return Markdown, JSON, dict, string, file path—anything serializable.
- **Multiple entrypoints:**
  - Dash app button
  - CLI/cron one-liner
  - Import and await as a coroutine
- **Async orchestration:** All agents run with async I/O; long API calls don't block others.

## Directory Layout
```
langgraph-workflow-template/
│
├─ workflow_core/           # Core orchestration (never edit these files)
│   ├─ __init__.py
│   ├─ orchestrator_core.py
│   └─ workflow_loader.py
│
├─ run_once.py             # CLI entrypoint / cron target
├─ dash_app.py             # Dash button demo
│
├─ config/
│   └─ workflow.yaml       # 🚨 non-coders edit only this file
│
└─ agents/                 # one file per real AI module
    ├─ belief.py
    ├─ observation.py
    ├─ interpretation.py
    ├─ insight.py
    ├─ hypothesis.py
    ├─ recommendation.py
    └─ __init__.py
```

## User Manual
| Step                  | What non-coder does                                                                 | File(s)                |
|-----------------------|-------------------------------------------------------------------------------------|------------------------|
| Add a new agent       | 1. Create `agents/new_feature.py` with `async def run(...) -> <any python value>`.<br>2. Append a YAML block under `agents:` specifying module, func, inputs, outputs.<br>3. Wire its parents/children in `edges`. | agents/*.py, config/workflow.yaml |
| Change execution order| Edit the `edges:` section – same parent list → parallel; different parent → sequential. | workflow.yaml          |
| Change data keys      | Update `outputs:` and any downstream `inputs:` lists in YAML.                        | workflow.yaml          |
| No Python edits needed| The loader auto-creates/updates the State type, node wrappers, and the compiled graph.| (done automatically)   |
| Run manually          | `python run_once.py <customer_id>`                                                  | CLI or cron            |
| Run via Dash          | (already wired) – user clicks the button                                            | dash_app.py            |
| Environment vars      | Expose anything agents need (e.g. OPENAI_API_KEY, FAST_API_URL) in the shell or Dash secrets. | –                      |

## Example: Add a New Agent
1. Create `agents/my_agent.py` with an async `run` function.
2. Add a block to `config/workflow.yaml` under `agents:` and wire it in `edges:`.
3. No Python code changes required.

## Debugging
Debug individual agents by running them directly:
```
python -m agents.observation DEMO-CUST
```

## Requirements
- Python 3.8+
- `langgraph`, `pyyaml`, `dash`

## Install dependencies
```
pip install langgraph pyyaml dash
```

## Run the workflow
```
python run_once.py CUST-12345
```

## Run the Dash app
```
python dash_app.py
```

---

**Note:**
- Keep `outputs:` keys unique unless you want parallel branches writing to the same key (then add a reducer manually in code).
- All tasks run with async I/O.
- Agents can return Markdown, JSON, dicts, or strings. The wrapper in `workflow_loader.py` just sticks the value into the shared state; downstream nodes decide how to interpret it. 