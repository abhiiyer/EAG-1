# decision.py

# decision.py
from agentSession import AgentSession

class DecisionAgent:
    def __init__(self):
        self.session = AgentSession()
        self.failure_threshold = 2

    def create_plan(self, entities):
        """
        This method receives entities and creates a structured plan for execution.
        """
        steps = []
        print(f"[INFO] Creating Plan for Entities: {entities}")
        
        # Step 1: Determine the action based on entities
        for entity, value in entities:
            if entity == "BalanceTrend":
                steps.append({
                    "action": "Check FX Engagement",
                    "tool": "transaction_analysis",
                    "params": {"type": "FX Engagement"}
                })
            
            elif entity == "FDMaturityDate":
                steps.append({
                    "action": "Notify FD Maturity",
                    "tool": "fd_analysis",
                    "params": {"type": "FD Maturity Alert"}
                })
            
            elif entity == "CompetitorRates":
                print(f"[INFO] Adding Competitor Rate Check to Plan")
                steps.append({
                    "action": "Compare FD Rates",
                    "tool": "competitor_intelligence",
                    "params": {"query": "best FD rates in UAE"}
                })
        
        # Step 2: Choose Strategy based on Failure Count
        strategy = self._choose_strategy(steps)
        
        # Step 3: Build a structured plan
        plan = {
            "strategy": strategy,
            "steps": steps,
            "current_step": 0
        }

        # ✅ Log Step History
        for step in steps:
            self.session.update_step_history(step['action'], "Created")

        # ✅ Save logs
        self.session.save_logs()
        
        print(f"[INFO] Final Strategy Chosen: {strategy}")
        return plan

    def _choose_strategy(self, steps):
        """
        Choose strategy based on failure rate and execution state
        """
        conservative_failures = 0
        exploratory_failures = 0

        for step in steps:
            action = step["action"]
            confidence_data = self.session.session_data["confidence_levels"].get(action, {"success": 0, "failure": 0})
            if confidence_data["failure"] >= self.failure_threshold:
                if step["tool"] == "competitor_intelligence":
                    exploratory_failures += 1
                else:
                    conservative_failures += 1
        
        if conservative_failures > 0:
            self.session.log_strategy_transition("Conservative", "Exploratory", "Multiple Failures Detected")
            self.session.save_logs()
            return "Exploratory"
        
        elif exploratory_failures > 0:
            self.session.log_strategy_transition("Exploratory", "Fallback", "Critical Failures Detected")
            self.session.save_logs()
            return "Fallback"
        
        else:
            return "Conservative"


'''
from agentSession import AgentSession

class DecisionAgent:
    def __init__(self):
        self.session = AgentSession()
        self.failure_threshold = 2

    def create_plan(self, entities):
        """
        This method receives entities and creates a structured plan for execution.
        """
        steps = []
        print(f"[INFO] Creating Plan for Entities: {entities}")
        
        # Step 1: Determine the action based on entities
        for entity, value in entities:
            if entity == "BalanceTrend":
                steps.append({
                    "action": "Check FX Engagement",
                    "tool": "transaction_analysis",
                    "params": {"type": "FX Engagement"}
                })
            
            elif entity == "FDMaturityDate":
                steps.append({
                    "action": "Notify FD Maturity",
                    "tool": "fd_analysis",
                    "params": {"type": "FD Maturity Alert"}
                })
            
            elif entity == "CompetitorRates":
                print(f"[INFO] Adding Competitor Rate Check to Plan")
                steps.append({
                    "action": "Compare FD Rates",
                    "tool": "competitor_intelligence",
                    "params": {"query": "best FD rates in UAE"}
                })
        
        # Step 2: Choose Strategy based on Failure Count
        strategy = self._choose_strategy(steps)
        
        # Step 3: Build a structured plan
        plan = {
            "strategy": strategy,
            "steps": steps,
            "current_step": 0
        }

        # ✅ Log Step History
        for step in steps:
            self.session.update_step_history(step['action'], "Created")

        # ✅ Save logs
        self.session.save_logs()
        
        print(f"[INFO] Final Strategy Chosen: {strategy}")
        return plan

    def _choose_strategy(self, steps):
        """
        Choose strategy based on failure rate and execution state
        """
        conservative_failures = 0
        exploratory_failures = 0

        for step in steps:
            action = step["action"]
            confidence_data = self.session.session_data["confidence_levels"].get(action, {"success": 0, "failure": 0})
            if confidence_data["failure"] >= self.failure_threshold:
                if step["tool"] == "competitor_intelligence":
                    exploratory_failures += 1
                else:
                    conservative_failures += 1
        
        if conservative_failures > 0:
            print("[STRATEGY] Switching to Exploratory Mode")
            return "Exploratory"
        elif exploratory_failures > 0:
            print("[STRATEGY] Switching to Fallback Mode")
            return "Fallback"
        else:
            return "Conservative"
'''