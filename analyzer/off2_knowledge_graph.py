from serpapi import GoogleSearch
def analyze(query: str) -> dict:
    params = {
        "engine": "google",
        "q": query,
        "api_key": "8110e188bd4c38ac4553dadff357f1d9a84986a16fabb4564651ae018f9f9179"
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        kg = results.get("knowledge_graph")
        found = bool(kg)

        score = 100 if found else 0
        return {
            "score": score,
            "knowledge_graph_found": found,
            "title": kg.get("title") if kg else None
        }

    except Exception as e:
        return {
            "score": 0,
            "knowledge_graph_found": False,
            "error": str(e)
        }
