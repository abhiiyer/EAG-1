# action.py: Executes the final recommendation output from the RM Assist agent

from models import RMDecision

def execute_action(decision: RMDecision):
    print("\n[AGENT ACTION]")
    print("Suggested Action:", decision.suggested_action)
    print("Message to RM:", decision.message)