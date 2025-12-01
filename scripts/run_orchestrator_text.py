#!/usr/bin/env python3
"""
Simple runner to invoke the orchestrator and print a plain-text report.

Usage:
    source .venv/bin/activate
    python scripts/run_orchestrator_text.py "Plan for the next 7 days — expected Diwali crowds and high pollution levels in Delhi"
"""
import sys
import asyncio
import inspect

from src.agents.builder import get_hospital_orchestrator


def main():
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "Plan for the next 7 days — expected Diwali crowds and high pollution levels in Delhi"
    )

    # Build orchestrator (this configures the Gemini client)
    orchestrator = get_hospital_orchestrator()

    # Call the agent. The ADK may expose a synchronous or asynchronous call.
    try:
        result = orchestrator.run(prompt)
    except TypeError:
        # Some ADK versions require run_async or return coroutine
        result = getattr(orchestrator, "run", None)
        if result is None:
            print("The orchestrator does not expose a 'run' method in this environment.")
            sys.exit(1)
        result = result(prompt)

    if inspect.isawaitable(result):
        out = asyncio.run(result)
    else:
        out = result

    # Print whatever the agent returned (likely plain-text). If it's an object, print repr.
    try:
        print(out)
    except Exception:
        print(repr(out))


if __name__ == "__main__":
    main()
