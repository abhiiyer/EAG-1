from agentSession import AgentSession
from tools.transaction_analysis import TransactionAnalysis
from tools.fd_analysis import FDAnalysis
#from tools.mcp_competitor_intelligence import MCPCompetitorIntelligence
from tools.competitor_intelligence import MCPCompetitorIntelligence
from decision import DecisionAgent
import time
import os
import sys

class ExecutorAgent:
    def __init__(self):
        self.session = AgentSession()
        self.transaction_analyzer = TransactionAnalysis()
        self.fd_analyzer = FDAnalysis()
        self.competitor_intel = MCPCompetitorIntelligence()
        self.max_retries = 3
        self.max_replans = 2

    def execute_plan(self, plan, attempt=1):
        print(f"\n[INFO] Starting Execution of Plan (v{attempt}): {plan['strategy']}")
        print(f"{'-'*50}\n")

        strategy = plan.get("strategy", "Conservative")
        steps = plan.get("steps", [])

        if strategy == "Conservative":
            success, results = self._execute_sequential(steps)
        elif strategy == "Exploratory":
            success, results = self._execute_parallel(steps)
        else:
            success, results = self._execute_fallback(steps)

        if not success and attempt < self.max_replans:
            print(f"[INFO] Triggering Adaptive Replan (Attempt {attempt + 1})")
            updated_entities = self._extract_entities(results)
            new_plan = DecisionAgent().create_plan(updated_entities)
            return self.execute_plan(new_plan, attempt=attempt + 1)

        print("[INFO] Execution Completed")

        if __name__ == "__main__" or "simulator" not in sys.argv[0].lower():
            os.system("python final_diagnostic_report.py")
            os.system("python dashboard_generator.py")
            os.system("python archiver.py")

        return results

    def _execute_sequential(self, steps):
        results = {}
        plan_failed = False

        for step in steps:
            action = step["action"]
            tool = step["tool"]
            params = step.get("params", {})
            success, output = self._run_step(tool, action, params)
            results[action] = output
            if not success:
                plan_failed = True

        return not plan_failed, results

    def _execute_parallel(self, steps):
        results = {}
        plan_failed = False

        for step in steps:
            action = step["action"]
            tool = step["tool"]
            params = step.get("params", {})
            print(f"[INFO] Executing {tool} for '{action}' in parallel (simulated)")
            success, output = self._run_step(tool, action, params)
            results[action] = output
            if not success:
                plan_failed = True

        return not plan_failed, results

    def _execute_fallback(self, steps):
        results = {}
        for step in steps:
            action = step["action"]
            tool = step["tool"]
            print(f"[FALLBACK] Simplified fallback for: {action}")
            output = {"status": "Simplified fallback executed"}
            self.session.log_execution(action, "Fallback", output)
            self.session.save_logs()
            results[action] = output
        return True, results

    def _run_step(self, tool_name, action, params):
        retry_count = 0
        result = None

        while retry_count < self.max_retries:
            try:
                if tool_name == "transaction_analysis":
                    result = self.transaction_analyzer.analyze_transactions("12345")
                elif tool_name == "fd_analysis":
                    result = self.fd_analyzer.check_fd_maturity("12345")
                elif tool_name == "competitor_intelligence":
                    result = self.competitor_intel.fetch_rates(params['query'])

                if result is None or not bool(result) or (isinstance(result, dict) and result.get("status") == "HITL Required"):
                    raise ValueError("Invalid or HITL result — not a success")

                # Only reached if success is confirmed
                self.session.update_step_history(action, "Success")
                self.session.update_confidence(action, True)
                self.session.log_tool_performance(tool_name, True)
                self.session.log_execution(action, "Success", result)
                self.session.save_logs()
                return True, result


            except Exception as e:
                print(f"[ERROR] Failed: {action} - {e}")
                retry_count += 1
                self.session.update_step_history(action, "Failure")
                self.session.update_confidence(action, False)
                self.session.log_tool_performance(tool_name, False)
                self.session.log_execution(action, "Failed", {"error": str(e)})
                self.session.log_human_intervention(tool_name, f"Retry {retry_count}")
                self.session.save_logs()

        # HITL fallback logic — central rollback
        self.session.log_human_intervention(tool_name, f"Max retries reached for {action}")
        self.session.force_rollback(action, tool_name)
        return False, {"status": "HITL Required"}

    def _extract_entities(self, result_map):
        entities = []
        if 'Check FX Engagement' in result_map:
            entities.append(("BalanceTrend", "Stable"))
        if 'Notify FD Maturity' in result_map:
            entities.append(("FDMaturityDate", "No FD Found"))
        if 'Compare FD Rates' in result_map:
            entities.append(("CompetitorRates", ["https://example.com"]))
        return entities
