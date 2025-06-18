import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

SERPAPI_KEY = "8110e188bd4c38ac4553dadff357f1d9a84986a16fabb4564651ae018f9f9179"  # klucz API

def get_people_also_ask(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "hl": "pl"
    }

    try:
        res = requests.get(url, params=params)
        data = res.json()
        questions = [item.get("question") for item in data.get("related_questions", []) if item.get("question")]
        return questions[:10]
    except Exception as e:
        print(f"[BŁĄD] SerpAPI: {e}")
        return []

def extract_faq_questions_from_html(html: str):
    soup = BeautifulSoup(html, "html.parser")
    headers = soup.find_all(["h2", "h3"])
    return [h.get_text(strip=True) for h in headers if "?" in h.get_text()]

def analyze(html: str, url: str) -> int:
    base_query = url.split("//")[-1].split("/")[0]  
    paa_questions = get_people_also_ask(base_query)
    faq_questions = extract_faq_questions_from_html(html)

    if not paa_questions or not faq_questions:
        return 0

    matches = 0
    for paa in paa_questions:
        for faq in faq_questions:
            similarity = fuzz.token_set_ratio(paa.lower(), faq.lower())
            if similarity >= 80:
                matches += 1
                break  

    score = round((matches / len(paa_questions)) * 100)
    return score
