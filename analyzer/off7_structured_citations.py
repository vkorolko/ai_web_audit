from bs4 import BeautifulSoup
def analyze(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    sameas = soup.find_all("link", rel="me")
    jsonld = soup.find_all("script", type="application/ld+json")

    count = len(sameas) + len(jsonld)
    score = 100 if count >= 2 else 0

    return {
        "score": score,
        "citation_elements_found": count
    }
