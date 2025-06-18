from bs4 import BeautifulSoup
def analyze(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    has_main = bool(soup.find("main"))
    has_footer = bool(soup.find("footer"))
    score = 100 if has_main and has_footer else 0

    return {
        "score": score,
        "has_main": has_main,
        "has_footer": has_footer
    }
