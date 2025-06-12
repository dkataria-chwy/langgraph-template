from dash import Dash, html, dcc, Input, Output, State as DS
import asyncio, json
from workflow_core.workflow_loader import run_workflow

app = Dash(__name__)

app.layout = html.Div(
    [
        dcc.Input(id="cid", placeholder="Customer ID"),
        html.Button("Run Workflow", id="go"),
        html.Pre(id="out", style={"whiteSpace": "pre-wrap"}),
    ]
)

@app.callback(Output("out", "children"),
              Input("go", "n_clicks"),
              DS("cid", "value"),
              prevent_initial_call=True)
def launch(_, cid):
    if not cid:
        return "Enter customer ID!"
    final = asyncio.run(run_workflow(customer_id=cid))
    return json.dumps(
        {
            "recommendations": final.get("recommendations"),
            "insights_md": final.get("insights_md"),
        },
        indent=2,
    )

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050) 