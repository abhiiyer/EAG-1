# main.py - Interactive Query Pipeline
from planner import run_planner_agent
from retriever import run_retriever_agent
from thinker import run_thinker_agent
from coder import run_coder_agent
from formatter import run_formatter_agent
from clarifier import clarify_query
from distiller import distill_article
from qa import answer_question_from_html
from summarizer import summarize_html_report



def run_pipeline(user_query):
    print("\n🧭 Step 1: PlannerAgent")
    plan = run_planner_agent(user_query)

    print("\n✅ Final Plan Graph:")
    for node in plan.get("nodes", []):
        print(f"- Step {node['id']}: {node['description']} [{node['agent']}]")

    print("\n➡️ Edges:")
    for edge in plan.get("edges", []):
        print(f"{edge['source']} → {edge['target']}")

    print("\n🔍 Step 2: RetrieverAgent")
    articles = run_retriever_agent(user_query, top_n=3)
    if not articles:
        print("No articles retrieved. Try another query.")
        return

    for i, a in enumerate(articles, 1):
        distilled = distill_article(a['content'])
        print(f"\n📄 Article {i} ({a['url']}):\n", distilled[:500])
        a['content'] = distilled  # replace original with distilled version

        #print(f"\n📄 Article {i} ({a['url']}):\n", a['content'][:400])

    print("\n🧠 Step 3: ThinkerAgent")
    insights = run_thinker_agent(articles)
    for theme, points in insights.items():
        print(f"\n🔹 {theme}")
        for p in points:
            print(" -", p)

    print("\n🛠️ Step 4: CoderAgent")
    final_html, _ = run_coder_agent(insights)

    print("\n🎨 Step 5: FormatterAgent")
    formatted_html = run_formatter_agent(final_html)
    
    # 🧾 Save Executive Summary
    summary = summarize_html_report(formatted_html)

    print("\n✅ Final report saved in outputs/formatted_report.html")
    
    # Ask if user wants Q&A
    while True:
        follow_up = input("\n❓ Ask a follow-up question about the report (or press Enter to skip): ").strip()
        if not follow_up:
            break
        answer = answer_question_from_html(follow_up, formatted_html)
        print(f"\n💬 Answer:\n{answer}")

if __name__ == "__main__":
    print("📊 Welcome to the Mashreq Strategy Copilot")
    while True:
        user_query = input("\n🔎 Ask a question or type 'exit': ").strip()
        if user_query.lower() == "exit":
            print("👋 Goodbye!")
            break
        clarified_query = clarify_query(user_query)
        run_pipeline(user_query)
