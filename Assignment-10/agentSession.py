
# agentSession.py
import json
from datetime import datetime

class AgentSession:
    def __init__(self):
        self.session_data = {
            "plan_versions": [],
            "tool_performance": {},
            "execution_log": [],
            "human_intervention": [],
            "step_history": {},
            "confidence_levels": {},
            "strategy_transitions": []
        }
        self.max_steps = 3
        self.max_retries = 3

    def update_step_history(self, step, status):
        """
        Update the step history log with the current step and its status.
        """
        if step not in self.session_data["step_history"]:
            self.session_data["step_history"][step] = []
        
        history_entry = {
            "timestamp": str(datetime.now()),
            "status": status
        }
        self.session_data["step_history"][step].append(history_entry)


    def update_confidence(self, step, success):
        if step not in self.session_data["confidence_levels"]:
            self.session_data["confidence_levels"][step] = {"success": 0, "failure": 0}
        
        if success:
            self.session_data["confidence_levels"][step]["success"] += 1
        else:
            self.session_data["confidence_levels"][step]["failure"] += 1


    def log_tool_performance(self, tool_name, success=True):
        if tool_name not in self.session_data["tool_performance"]:
            self.session_data["tool_performance"][tool_name] = {"success": 0, "failure": 0}
        
        if success:
            self.session_data["tool_performance"][tool_name]["success"] += 1
        else:
            self.session_data["tool_performance"][tool_name]["failure"] += 1
    
    def log_execution(self, step, status, result):
        log_entry = {
            "timestamp": str(datetime.now()),
            "step": step,
            "status": status,
            "result": result
        }
        self.session_data["execution_log"].append(log_entry)

    def log_strategy_transition(self, from_strategy, to_strategy, reason):
        """
        Log when a strategy transition occurs
        """
        log_entry = {
            "timestamp": str(datetime.now()),
            "from_strategy": from_strategy,
            "to_strategy": to_strategy,
            "reason": reason
        }
        print(f"[STRATEGY TRANSITION] Switching from {from_strategy} → {to_strategy}")
        self.session_data["strategy_transitions"].append(log_entry)
        
        
    def log_human_intervention(self, tool_name, reason):
        intervention_entry = {
            "timestamp": str(datetime.now()),
            "tool_name": tool_name,
            "reason": reason
        }
        self.session_data["human_intervention"].append(intervention_entry)

    def force_rollback(self, action, tool_name):
        """
        Removes incorrect 'Success' marks and logs HITL failure.
        """
        print(f"[HITL] Forcing rollback for action '{action}' and tool '{tool_name}'")

        # Step history cleanup
        if action in self.session_data["step_history"]:
            filtered = [
                entry for entry in self.session_data["step_history"][action]
                if entry["status"] != "Success"
            ]
            removed = len(self.session_data["step_history"][action]) - len(filtered)
            self.session_data["step_history"][action] = filtered
            print(f"[DEBUG] Removed {removed} Success entries from step_history")

        # Add HITL Failure
        self.update_step_history(action, "HITL Failure")

        # Confidence rollback
        if action in self.session_data["confidence_levels"]:
            if self.session_data["confidence_levels"][action]["success"] > 0:
                self.session_data["confidence_levels"][action]["success"] -= 1
                self.session_data["confidence_levels"][action]["failure"] += 1
                print(f"[DEBUG] Adjusted confidence_levels for {action}")

        # Tool performance rollback
        if tool_name in self.session_data["tool_performance"]:
            if self.session_data["tool_performance"][tool_name]["success"] > 0:
                self.session_data["tool_performance"][tool_name]["success"] -= 1
                self.session_data["tool_performance"][tool_name]["failure"] += 1
                print(f"[DEBUG] Adjusted tool_performance for {tool_name}")

        self.save_logs()

    def save_logs(self):
        """
        Force writes to disk for each log type
        """
        with open("./logs/tool_performance.log", "w") as f:
            f.write(json.dumps(self.session_data["tool_performance"], indent=4))
        with open("./logs/plan_execution.log", "w") as f:
            f.write(json.dumps(self.session_data["execution_log"], indent=4))
        with open("./logs/human_in_loop.log", "w") as f:
            f.write(json.dumps(self.session_data["human_intervention"], indent=4))
        with open("./logs/step_history.log", "w") as f:
            f.write(json.dumps(self.session_data["step_history"], indent=4))
        with open("./logs/confidence_levels.log", "w") as f:
            f.write(json.dumps(self.session_data["confidence_levels"], indent=4))
        with open("./logs/strategy_transitions.log", "w") as f:
            f.write(json.dumps(self.session_data["strategy_transitions"], indent=4))


'''
class AgentSession:
    def __init__(self):
        self.session_data = {
            "plan_versions": [],
            "tool_performance": {},
            "execution_log": [],
            "human_intervention": [],
            "step_history": {},
            "confidence_levels": {}
        }
        self.max_steps = 3
        self.max_retries = 3

    def update_step_history(self, step, status):
        """
        Update the step history log with the current step and its status.
        """
        if step not in self.session_data["step_history"]:
            self.session_data["step_history"][step] = []
        
        history_entry = {
            "timestamp": str(datetime.now()),
            "status": status
        }
        self.session_data["step_history"][step].append(history_entry)

    def log_tool_performance(self, tool_name, success=True):
        if tool_name not in self.session_data["tool_performance"]:
            self.session_data["tool_performance"][tool_name] = {"success": 0, "failure": 0}
        
        if success:
            self.session_data["tool_performance"][tool_name]["success"] += 1
        else:
            self.session_data["tool_performance"][tool_name]["failure"] += 1
    
    def log_execution(self, step, status, result):
        log_entry = {
            "timestamp": str(datetime.now()),
            "step": step,
            "status": status,
            "result": result
        }
        self.session_data["execution_log"].append(log_entry)

    def log_human_intervention(self, tool_name, reason):
        intervention_entry = {
            "timestamp": str(datetime.now()),
            "tool_name": tool_name,
            "reason": reason
        }
        self.session_data["human_intervention"].append(intervention_entry)

    def save_logs(self):
        """
        Force writes to disk for each log type
        """
        with open("./logs/tool_performance.log", "w") as f:
            f.write(json.dumps(self.session_data["tool_performance"], indent=4))
        with open("./logs/plan_execution.log", "w") as f:
            f.write(json.dumps(self.session_data["execution_log"], indent=4))
        with open("./logs/human_in_loop.log", "w") as f:
            f.write(json.dumps(self.session_data["human_intervention"], indent=4))
        with open("./logs/step_history.log", "w") as f:
            f.write(json.dumps(self.session_data["step_history"], indent=4))
        with open("./logs/confidence_levels.log", "w") as f:
            f.write(json.dumps(self.session_data["confidence_levels"], indent=4))

    def update_confidence(self, step, success):
        if step not in self.session_data["confidence_levels"]:
            self.session_data["confidence_levels"][step] = {"success": 0, "failure": 0}
        
        if success:
            self.session_data["confidence_levels"][step]["success"] += 1
        else:
            self.session_data["confidence_levels"][step]["failure"] += 1

    def force_rollback(self, action, tool_name):
        """
        Force rollback for HITL scenarios and flush logs to disk
        """
        print(f"[HITL] Forcing rollback for {action} and {tool_name}")

        # 🚀 Remove "Success" if it was logged
        history = self.session_data["step_history"].get(action, [])
        
        # ✅ Remove all "Success" entries
        filtered_history = [entry for entry in history if entry["status"] != "Success"]
        self.session_data["step_history"][action] = filtered_history
        
        # ✅ Mark it as "HITL Failure"
        self.update_step_history(action, "HITL Failure")
        
        # ✅ Correct tool performance if incorrectly marked
        if self.session_data["tool_performance"].get(tool_name, {}).get("success", 0) > 0:
            print(f"[CRITICAL] Rolling back Success for {tool_name}")
            self.session_data["tool_performance"][tool_name]["success"] -= 1
            self.session_data["tool_performance"][tool_name]["failure"] += 1
        
        # ✅ Remove "Success" from confidence
        if self.session_data["confidence_levels"].get(action, {}).get("success", 0) > 0:
            self.session_data["confidence_levels"][action]["success"] -= 1
            self.session_data["confidence_levels"][action]["failure"] += 1
        
        # ✅ Immediate Forced Flush to Disk
        print(f"[CRITICAL] Forcing Flush to Disk for HITL Correction")
        
        # 🚀 Flush Each Log Individually
        with open("./logs/tool_performance.log", "w") as f:
            f.write(json.dumps(self.session_data["tool_performance"], indent=4))
        with open("./logs/step_history.log", "w") as f:
            f.write(json.dumps(self.session_data["step_history"], indent=4))
        with open("./logs/confidence_levels.log", "w") as f:
            f.write(json.dumps(self.session_data["confidence_levels"], indent=4))
        
        # 🚀 Read back from disk to ensure it's clean
        with open('./logs/step_history.log', 'r') as f:
            self.session_data["step_history"] = json.load(f)
        
        with open('./logs/confidence_levels.log', 'r') as f:
            self.session_data["confidence_levels"] = json.load(f)

        with open('./logs/tool_performance.log', 'r') as f:
            self.session_data["tool_performance"] = json.load(f)

        print(f"[INFO] Rollback successful for {action}")
'''

