from serpapi import GoogleSearch
from urllib.parse import urlparse
def analyze(url: str) -> dict:
    domain = urlparse(url).netloc

    params = {
        "engine": "google",
        "q": f"site:{domain}",
        "api_key": "8110e188bd4c38ac4553dadff357f1d9a84986a16fabb4564651ae018f9f9179"
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()

        #sprawodzanie czy jest w google
        organic_results = results.get("organic_results", [])
        found = len(organic_results) > 0

        score = 100 if found else 0

        return {
            "score": score,
            "domain": domain,
            "results_found": len(organic_results),
            "message": "Szukano w Google za pomocą SerpAPI"
        }

    except Exception as e:
        return {
            "score": 0,
            "domain": domain,
            "error": str(e)
        }
