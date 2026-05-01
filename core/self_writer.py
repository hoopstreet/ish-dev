#!/usr/bin/env python3
import os
from ai.router import ask

MODULE_DIR="/root/ish-dev/modules"

def generate_module(task):
    prompt=f"""
Create a production-ready Python module for:

TASK:
{task}

Rules:
- no explanations
- only code
- must be reusable module
"""

    code=ask(prompt)

    if not code:
        return None

    filename=f"{MODULE_DIR}/auto_{abs(hash(task))}.py"

    with open(filename,"w") as f:
        f.write(code)

    return filename
