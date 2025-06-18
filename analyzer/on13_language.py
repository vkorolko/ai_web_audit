from bs4 import BeautifulSoup
def analyze(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    html_tag = soup.find("html")
    lang = html_tag.get("lang") if html_tag else None
    score = 100 if lang else 0

    return {
        "score": score,
        "lang": lang or "not set"
    }
