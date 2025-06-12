"""
Run the whole workflow once from the command-line or a cron job:
$ python run_once.py CUST-12345
"""

import sys, asyncio, json
from workflow_core.workflow_loader import run_workflow

customer_id = sys.argv[1] if len(sys.argv) > 1 else "DEMO-CUST"

final_state = asyncio.run(run_workflow(customer_id=customer_id))
print(json.dumps(final_state, indent=2)) 