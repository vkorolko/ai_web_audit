import requests

PSI_API_KEY = "" #klucz PSI_API

def analyze(url: str) -> int:
    api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "key": PSI_API_KEY,
        "strategy": "desktop"
    }

    try:
        response = requests.get(api_url, params=params)
        data = response.json()

        audits = data["lighthouseResult"]["audits"]
        lcp = audits.get("largest-contentful-paint", {}).get("score", 0)
        inp = audits.get("interaction-to-next-paint", {}).get("score", 0)
        cls = audits.get("cumulative-layout-shift", {}).get("score", 0)
        score = round((lcp + inp + cls) / 3 * 100)
        return score

    except Exception as e:
        print(f"[BŁĄD] PageSpeed API: {e}")
        return 0
