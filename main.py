import argparse
import os
import json
from datetime import datetime
import nltk

from utils.loader import fetch_html #import dla HTML
from analyzer import on1_qa_structure, on2_jsonld, on3_eeat, on4_sources, on5_alt_texts, on6_freshness


REPORT_DIR = "reports"

def ensure_nltk_resources():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("[INFO]")
        nltk.download('punkt')

def run_analysis(url: str):
    print(f"[INFO] analiza URL: {url}")

    html = fetch_html(url)
    if html is None:
        print(f"[ERROR]  {url}")
        return

    results = {
        "url": url,
        "timestamp": datetime.utcnow().isoformat(),
        "scores": {}
    }

    # ON1
    print("[RUNNING] ON1: Frage-Antwort Struktur")
    results["scores"]["ON1"] = on1_qa_structure.analyze(html)

    # ON2
    print("[RUNNING] ON2: Strukturierte Daten")
    results["scores"]["ON2"] = on2_jsonld.analyze(html)
     
    # ON3
    print("[RUNNING] ON3: EEAT & Autorenschaft")
    results["scores"]["ON3"] = on3_eeat.analyze(html, url)

    #ON4
    print("[RUNNING] ON4: Quellenangaben (Sources)")
    results["scores"]["ON4"] = on4_sources.analyze(html, url)

    #ON5
    print("[RUNNING] ON5: ALT-Texte bei Bildern")
    results["scores"]["ON5"] = on5_alt_texts.analyze(html)

    #ON6
    print("[RUNNING] ON6: Aktualität")
    results["scores"]["ON6"] = on6_freshness.analyze(html, url)

    save_report(url, results)

def save_report(url: str, data: dict):
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

    safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")
    filename = f"{safe_url}.json"
    filepath = os.path.join(REPORT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"[OK] Raport  {filepath}")

def main():
    ensure_nltk_resources()
    parser = argparse.ArgumentParser(description="AI Web Audit Tool")
    parser.add_argument("url", help="URL strony")
    args = parser.parse_args()
    run_analysis(args.url)

if __name__ == "__main__":
    main()
