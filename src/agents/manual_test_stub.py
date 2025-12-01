# src/manual_test_stub.py
"""
Manual stub to show how you *might* call the orchestrator.

Check your google-adk docs for the correct method to invoke an LlmAgent,
then replace the TODO section below.
"""

from src.agents.builder import get_hospital_orchestrator

def main():
    orchestrator = get_hospital_orchestrator()

    # TODO: Replace this with the actual ADK invocation API, e.g.:
    # response = orchestrator.run("Plan for the next 7 days for Diwali week.")
    # print(response)

    print(
        "Orchestrator agent constructed successfully. "
        "Now check your google-adk docs for how to invoke LlmAgent."
    )

if __name__ == "__main__":
    main()
