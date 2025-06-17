from bs4 import BeautifulSoup
import requests

def analyze(html: str, url: str = "") -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # 
    bio = soup.select_one(".author-bio")
    bio_word_count = len(bio.get_text(strip=True).split()) if bio else 0
    bio_score = 100 if bio_word_count >= 75 else 0

    author_link_score = 0
    author_href = None
    author_link = soup.find("a", rel="author")
    if author_link and author_link.get("href"):
        author_href = author_link["href"]
        try:
            response = requests.get(author_href, timeout=5)
            if response.status_code == 200:
                author_link_score = 100
        except Exception:
            pass
    https_score = 100 if url.startswith("https://") else 0
    final_score = round((0.4 * bio_score) + (0.4 * author_link_score) + (0.2 * https_score), 2)

    return {
        "score": final_score,
        "bio_word_count": bio_word_count,
        "bio_score": bio_score,
        "author_link": author_href,
        "author_link_score": author_link_score,
        "https_score": https_score
    }
