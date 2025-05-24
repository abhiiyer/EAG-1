# perception.py

'''
from tools.transaction_analysis import TransactionAnalysis
from tools.fd_analysis import FDAnalysis
from tools.competitor_intelligence import CompetitorIntelligence
from tools.document_search import DocumentSearch


class PerceptionAgent:
    def __init__(self):
        self.transaction_analyzer = TransactionAnalysis()
        self.fd_analyzer = FDAnalysis()
        self.competitor_intel = CompetitorIntelligence()
        self.document_search = DocumentSearch()

    def perceive(self, customer_id, query):
        entities = []
        print(f"[DEBUG] Query received: {query}")
        
        if "transaction" in query.lower():
            analysis = self.transaction_analyzer.analyze_transactions(customer_id)
            print(f"[DEBUG] Transaction Analysis Result: {analysis}")
            entities.append(("BalanceTrend", analysis["BalanceTrend"]))
            entities.append(("LastFXTransaction", analysis["LastFXTransaction"]))
        
        if "fd" in query.lower():
            fd_details = self.fd_analyzer.check_fd_maturity(customer_id)
            print(f"[DEBUG] FD Analysis Result: {fd_details}")
            entities.append(("FDMaturityDate", fd_details["FDMaturityDate"]))
        
        if "competitor" in query.lower():
            print(f"[DEBUG] Competitor Query Detected: {query}")
            rates = self.competitor_intel.fetch_rates("best FD rates in UAE")
            print(f"[DEBUG] Competitor Intelligence Result: {rates}")
            entities.append(("CompetitorRates", rates["SearchResults"] if rates else []))

        if "document" in query.lower():
            search_result = self.document_search.search_document("FD Rate", "FD_Rates_Q1_2025.pdf")
            entities.append(("DocumentSearch", search_result))

        print(f"[INFO] Perception Completed with Entities: {entities}")
        return entities
'''

# perception.py
from tools.transaction_analysis import TransactionAnalysis
from tools.fd_analysis import FDAnalysis
from tools.competitor_intelligence import MCPCompetitorIntelligence
from tools.document_search import DocumentSearch

class PerceptionAgent:
    def __init__(self):
        self.transaction_analyzer = TransactionAnalysis()
        self.fd_analyzer = FDAnalysis()
        self.competitor_intel = MCPCompetitorIntelligence()
        self.document_search = DocumentSearch()

    def perceive(self, customer_id, query):
        entities = []
        print(f"[DEBUG] Query received: {query}")
        
        if "transaction" in query.lower():
            analysis = self.transaction_analyzer.analyze_transactions(customer_id)
            entities.append(("BalanceTrend", analysis["BalanceTrend"]))
            entities.append(("LastFXTransaction", analysis["LastFXTransaction"]))
        
        if "fd" in query.lower():
            fd_details = self.fd_analyzer.check_fd_maturity(customer_id)
            entities.append(("FDMaturityDate", fd_details["FDMaturityDate"]))
        
        if "competitor" in query.lower():
            print(f"[DEBUG] Competitor Query Detected: {query}")
            rates = self.competitor_intel.fetch_rates("best FD rates in UAE")
            if "SearchResults" in rates:
                entities.append(("CompetitorRates", rates["SearchResults"]))
            else:
                entities.append(("CompetitorRates", ["HITL Required"]))

        if "document" in query.lower():
            search_result = self.document_search.search_document("FD Rate", "FD_Rates_Q1_2025.pdf")
            entities.append(("DocumentSearch", search_result))

        print(f"[INFO] Perception Completed with Entities: {entities}")
        return entities
