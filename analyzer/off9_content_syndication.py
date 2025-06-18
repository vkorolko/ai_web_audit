from bs4 import BeautifulSoup
def analyze(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    canonical = soup.find("link", rel="canonical")

    has_canonical = bool(canonical and canonical.get("href"))
    score = 100 if has_canonical else 0

    return {
        "score": score,
        "canonical_url": canonical["href"] if canonical else None
    }
