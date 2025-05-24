# simulator.py
import random
import time
import csv
from perception import PerceptionAgent
from decision import DecisionAgent
from executor import ExecutorAgent
from datetime import datetime

# Initialize Agents
perception_agent = PerceptionAgent()
decision_agent = DecisionAgent()
executor_agent = ExecutorAgent()

# Test case scenarios
TEST_CASES = [
    "Fetch transaction and FD details for RM",
    "Get competitor rates for FD",
    "Analyze FX transactions for RM",
    "Analyze FD renewals for RM",
    "Get FD maturity and competitor rates for RM"
]

# CSV Header
headers = ["Test Case", "Execution Time (s)", "Success", "HITL Triggered", "Details"]

# Initialize CSV
with open('./logs/simulator_log.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

def run_simulation():
    """
    Runs the simulation for 100 test cases and logs the result
    """
    print("\n[INFO] Starting Simulation of 100 Test Cases")
    print("--------------------------------------------------")
    
    for i in range(1, 30):
        print(f"[INFO] Running Test Case #{i}")
        
        try:
            # Randomly pick a test case
            test_case = random.choice(TEST_CASES)
            print(f"[DEBUG] Test Case Chosen: {test_case}")
            
            # Step 1: Perception Phase
            start_time = time.time()
            entities = perception_agent.perceive('12345', test_case)
            print(f"[DEBUG] Perception Result: {entities}")

            # Step 2: Decision Phase
            plan = decision_agent.create_plan(entities)
            print(f"[DEBUG] Plan Created: {plan}")

            # Step 3: Execution Phase
            results = executor_agent.execute_plan(plan)
            print(f"[DEBUG] Execution Result: {results}")
            end_time = time.time()

            # Calculate execution time
            exec_time = round(end_time - start_time, 2)

            # Determine if HITL was triggered
            hitl_triggered = "Yes" if "HITL Required" in str(results) else "No"

            # Log the details
            log_data = [test_case, exec_time, "Success", hitl_triggered, str(results)]
            print(f"[DEBUG] Log Data to Write: {log_data}")

            # Write to CSV
            with open('./logs/simulator_log.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(log_data)
                print(f"[INFO] Successfully wrote to CSV for Test Case #{i}")

            # Sleep to avoid rate limits
            time.sleep(1)

        except Exception as e:
            print(f"[ERROR] Exception occurred during simulation: {e}")

    print("\n[INFO] Simulation Completed. Results are stored in `./logs/simulator_log.csv`")
    print("--------------------------------------------------")

# Run the simulation
run_simulation()
