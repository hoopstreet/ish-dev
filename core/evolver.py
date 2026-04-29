from ai.router import ask

def evolve_codebase(summary):
    prompt=f"""
You are a system evolution engine.

Improve this system:

{summary}

Return:
- new feature idea
- implementation plan
- optional code module
"""
    return ask(prompt)
