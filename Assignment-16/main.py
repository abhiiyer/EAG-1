from planner import run_planner_agent

query = "Generate a strategy report comparing Mashreq Bank with FAB and ADCB in FX, Investments, and Insurance."
plan = run_planner_agent(query)

print("\n✅ Final Plan Graph:")
for node in plan.get("nodes", []):
    print(f"- Step {node['id']}: {node['description']} [{node['agent']}]")

print("\n➡️ Edges:")
for edge in plan.get("edges", []):
    print(f"{edge['source']} → {edge['target']}")


from retriever import run_retriever_agent
articles = run_retriever_agent("UAE bank deposit rates comparison", top_n=3)
for i, a in enumerate(articles, 1):
    print(f"\n📄 Article {i} ({a['url']}):\n", a['content'][:400])

from thinker import run_thinker_agent

insights = run_thinker_agent(articles)
print("\n🧠 Clustered Insights:")
for theme, points in insights.items():
    print(f"\n🔹 {theme}")
    for p in points:
        print(" -", p)


from coder import run_coder_agent

final_html, history = run_coder_agent(insights)


from formatter import run_formatter_agent

formatted_html = run_formatter_agent(final_html)
