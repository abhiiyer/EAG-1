# report_generator.py
import pandas as pd
import matplotlib.pyplot as plt
import json

# Load Data
simulator_log = pd.read_csv('./logs/simulator_log.csv')
with open('./logs/tool_performance.log') as f:
    tool_performance = json.load(f)
with open('./logs/human_in_loop.log') as f:
    human_in_loop = json.load(f)

# ========================
# 1️⃣ Summary Statistics
# ========================
print("\n=== Summary Statistics ===")
total_cases = len(simulator_log)
hitl_triggered = len(simulator_log[simulator_log['HITL Triggered'] == 'Yes'])
success_cases = total_cases - hitl_triggered

print(f"Total Test Cases: {total_cases}")
print(f"Successful Executions: {success_cases}")
print(f"HITL Triggered: {hitl_triggered}")

# ========================
# 2️⃣ Tool Performance
# ========================
print("\n=== Tool Performance ===")
tool_data = {"Tool": [], "Success": [], "Failure": [], "Executions": []}
for tool, data in tool_performance.items():
    total_executions = data['success'] + data['failure']
    print(f"{tool} -> Success: {data['success']}, Failure: {data['failure']}, Executions: {total_executions}")
    tool_data["Tool"].append(tool)
    tool_data["Success"].append(data['success'])
    tool_data["Failure"].append(data['failure'])
    tool_data["Executions"].append(total_executions)

# ========================
# 3️⃣ Visualization
# ========================
# Bar Chart - Tool Success vs. Failure
plt.figure(figsize=(8, 5))
plt.bar(tool_data["Tool"], tool_data["Success"], color='green', label='Success')
plt.bar(tool_data["Tool"], tool_data["Failure"], bottom=tool_data["Success"], color='red', label='Failure')
plt.title('Tool Performance: Success vs. Failure')
plt.xlabel('Tools')
plt.ylabel('Number of Executions')
plt.legend()
plt.savefig('./logs/tool_performance_summary.png')
plt.show()

# Pie Chart - HITL vs. Successful Runs
labels = ['Successful', 'HITL Required']
sizes = [success_cases, hitl_triggered]
colors = ['#4CAF50', '#FF6347']

plt.figure(figsize=(5, 5))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title('HITL vs. Successful Runs')
plt.savefig('./logs/hitl_summary.png')
plt.show()

# ========================
# 4️⃣ Save Summary Report
# ========================
with open('./logs/simulation_report.txt', 'w', encoding='utf-8') as f:
    f.write("=== Simulation Report ===\n")
    f.write(f"Total Test Cases: {total_cases}\n")
    f.write(f"Successful Executions: {success_cases}\n")
    f.write(f"HITL Triggered: {hitl_triggered}\n\n")
    f.write("=== Tool Performance ===\n")
    for tool, data in tool_performance.items():
        total_executions = data['success'] + data['failure']
        f.write(f"{tool} -> Success: {data['success']}, Failure: {data['failure']}, Executions: {total_executions}\n")

print("\n[INFO] Report generated successfully. Check './logs/simulation_report.txt'")
print("[INFO] Charts saved: 'tool_performance_summary.png' & 'hitl_summary.png'")
