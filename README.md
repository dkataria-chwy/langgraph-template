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

## Step-by-Step Guide

### 1. Clone the Repository
```bash
git clone https://github.com/dkataria-chwy/langgraph-template.git
cd langgraph-template
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Understanding the Workflow
The workflow is defined in `config/workflow.yaml`. This file contains:
- **Agents:** Each agent is a Python module with an async `run` function.
- **Edges:** Define the flow between agents.
- **Entry Point:** The first agent to run.

### 4. Adding a New Agent
1. **Create a new agent file** in the `agents/` directory. For example, `agents/my_agent.py`:
   ```python
   async def run(input_data):
       # Your agent logic here
       return {"output": "result"}
   ```

2. **Update `config/workflow.yaml`** to include the new agent:
   ```yaml
   agents:
     my_agent:
       module: agents.my_agent
       func: run
       outputs: ["output"]
       inputs: ["input_data"]
   ```

3. **Wire the agent** in the `edges` section:
   ```yaml
   edges:
     my_agent: []
   ```

### 5. Running the Workflow
- **CLI:** Run the workflow with a customer ID:
  ```bash
  python run_once.py CUST-12345
  ```

- **Dash App:** Start the Dash app and use the button to run the workflow:
  ```bash
  python dash_app.py
  ```

### 6. Debugging
Debug individual agents by running them directly:
```bash
python -m agents.my_agent
```

## Rules to Follow
- **Never edit `workflow_core/` files:** These files are the core orchestration logic and should not be modified.
- **Keep `outputs:` keys unique:** Unless you want parallel branches writing to the same key (then add a reducer manually in code).
- **All tasks run with async I/O:** Long API calls won't block other nodes.
- **Agents can return any serializable value:** Markdown, JSON, dict, string, file path—anything serializable.
- **Environment variables:** Expose anything agents need (e.g. OPENAI_API_KEY, FAST_API_URL) in the shell or Dash secrets.

## Example: Updating the YAML
Here's an example of how to update the `workflow.yaml` file to add a new agent:

### Before:
```yaml
agents:
  belief:
    module: agents.belief
    func: run
    outputs: ["belief_md"]
    inputs: ["customer_id"]
```

### After Adding a New Agent:
```yaml
agents:
  belief:
    module: agents.belief
    func: run
    outputs: ["belief_md"]
    inputs: ["customer_id"]
  my_agent:
    module: agents.my_agent
    func: run
    outputs: ["output"]
    inputs: ["input_data"]
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