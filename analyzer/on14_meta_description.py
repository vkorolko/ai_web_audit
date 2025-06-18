from bs4 import BeautifulSoup
def analyze(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    meta = soup.find("meta", attrs={"name": "description"})
    description = meta.get("content", "") if meta else ""
    score = 100 if len(description.strip()) >= 70 else 0

    return {
        "score": score,
        "description_length": len(description.strip()),
        "description": description.strip() or "not found"
    }
