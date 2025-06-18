import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def analyze(html: str, url: str = "https://example.com") -> dict:
    # Sprawdzenie robots.txt
    robots_url = urljoin(url, "/robots.txt")
    try:
        robots_resp = requests.get(robots_url, timeout=5)
        has_robots = robots_resp.status_code == 200
    except requests.RequestException:
        has_robots = False

    # Sprawdzenie meta tagu "robots" z wartością "noindex"
    soup = BeautifulSoup(html, "html.parser")
    robots_meta = soup.find("meta", attrs={"name": "robots"})
    contains_noindex = False
    if robots_meta and "noindex" in robots_meta.get("content", "").lower():
        contains_noindex = True
    score = 0
    if has_robots:
        score += 50
    if not contains_noindex:
        score += 50

    return {
        "score": score,
        "robots_txt_found": has_robots,
        "meta_robots_noindex": contains_noindex
    }
