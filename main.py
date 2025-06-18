import argparse
import os
import json
from datetime import datetime
import nltk

from utils.loader import fetch_html
from analyzer import (
    on1_qa_structure,
    on2_jsonld,on3_eeat,
    on4_sources,
    on5_alt_texts,
    on6_freshness,
    on7_intent,
    on8_core_web_vitals,
    on9_load_time,
    on10_robots,
    on11_structured_content,
    on12_media_elements,
    on13_language,
    on14_meta_description,
    on15_page_structure,
    off1_backlink_authority,
    off2_knowledge_graph,
    off3_serp_engagement,
    off4_social_signals,
    off5_reputation,
    off6_author_authority,
    off7_structured_citations,
    off8_expert_answers,
    off9_content_syndication,
    off10_public_apis
)

REPORT_DIR = "reports"

def ensure_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("[INFO] Downloading nltk punkt tokenizer")
        nltk.download('punkt')

def calculate_final_score(results: dict) -> float:
    scores = results["scores"]
    total = 0
    count = 0
    for key, val in scores.items():
        if isinstance(val, dict) and "score" in val:
            total += val["score"]
            count += 1
        elif isinstance(val, (int, float)):
            total += val
            count += 1
    return round(total / count, 2) if count > 0 else 0

def save_report(url: str, data: dict):
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

    safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
    filename = f"{safe_url}.json"
    filepath = os.path.join(REPORT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Raport zapisany: {filepath}")

def run_analysis(url: str):
    print(f"[INFO] analiza URL: {url}")

    html = fetch_html(url)
    if html is None:
        print(f"[ERROR] Nie można pobrać strony: {url}")
        return

    results = {
        "url": url,
        "timestamp": datetime.utcnow().isoformat(),
        "scores": {}
    }

    #ON1-ON15 OFF1-OFF10
    print("[URUCHAMIANIE] ON1: Struktura pytanie-odpowiedź")
    results["scores"]["ON1"] = on1_qa_structure.analyze(html)

    print("[URUCHAMIANIE] ON2: Dane strukturalne")
    results["scores"]["ON2"] = on2_jsonld.analyze(html)

    print("[URUCHAMIANIE] ON3: EEAT i autorstwo")
    results["scores"]["ON3"] = on3_eeat.analyze(html, url)

    print("[URUCHAMIANIE] ON4: Źródła zewnętrzne")
    results["scores"]["ON4"] = on4_sources.analyze(html, url)

    print("[URUCHAMIANIE] ON5: Teksty ALT w obrazach")
    results["scores"]["ON5"] = on5_alt_texts.analyze(html)

    print("[URUCHAMIANIE] ON6: Aktualność treści")
    results["scores"]["ON6"] = on6_freshness.analyze(html, url)

    print("[URUCHAMIANIE] ON7: Pokrycie intencji użytkownika")
    results["scores"]["ON7"] = on7_intent.analyze(html, url)

    print("[URUCHAMIANIE] ON8: Core Web Vitals")
    results["scores"]["ON8"] = on8_core_web_vitals.analyze(url)

    print("[RUNNING] ON9: Ladezeit")
    results["scores"]["ON9"] = on9_load_time.analyze(url=url)

    print("[RUNNING] ON10: Robots.txt & Indexierung")
    results["scores"]["ON10"] = on10_robots.analyze(html, url)

    print("[RUNNING] ON11: Strukturierter Content")
    results["scores"]["ON11"] = on11_structured_content.analyze(html)

    print("[RUNNING] ON12: Medienelemente")
    results["scores"]["ON12"] = on12_media_elements.analyze(html)

    print("[RUNNING] ON13: Sprache der Seite")
    results["scores"]["ON13"] = on13_language.analyze(html)

    print("[RUNNING] ON14: Meta Description")
    results["scores"]["ON14"] = on14_meta_description.analyze(html)

    print("[RUNNING] ON15: Seitenstruktur")
    results["scores"]["ON15"] = on15_page_structure.analyze(html)

    print("[RUNNING] OFF1: Backlink-Autorität (SerpAPI)")
    results["scores"]["OFF1"] = off1_backlink_authority.analyze(url)

    print("[RUNNING] OFF2: Knowledge Graph Mentions")
    results["scores"]["OFF2"] = off2_knowledge_graph.analyze(url)

    print("[RUNNING] OFF3: SERP Engagement")
    results["scores"]["OFF3"] = off3_serp_engagement.analyze()

    print("[RUNNING] OFF4: Social Signals")
    results["scores"]["OFF4"] = off4_social_signals.analyze()

    print("[RUNNING] OFF5: Reputation")
    results["scores"]["OFF5"] = off5_reputation.analyze()

    print("[RUNNING] OFF6: AutorAutorität")
    results["scores"]["OFF6"] = off6_author_authority.analyze()

    print("[RUNNING] OFF7: Strukturierte Citations")
    results["scores"]["OFF7"] = off7_structured_citations.analyze(html)

    print("[RUNNING] OFF8: Expertenantworten")
    results["scores"]["OFF8"] = off8_expert_answers.analyze()

    print("[RUNNING] OFF9: Content Syndication")
    results["scores"]["OFF9"] = off9_content_syndication.analyze(html)

    print("[RUNNING] OFF10: Public APIs")
    results["scores"]["OFF10"] = off10_public_apis.analyze()

    final_score = calculate_final_score(results)
    results["final_score"] = final_score
    print(f"\n[FINAL SCORE] Całkowity wynik audytu: {final_score}/100")

    save_report(url, results)

def main():
    ensure_nltk_resources()
    parser = argparse.ArgumentParser(description="AI Web Audit Tool")
    parser.add_argument("url", help="URL strony")
    args = parser.parse_args()
    run_analysis(args.url)

if __name__ == "__main__":
    main()
