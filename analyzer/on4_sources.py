from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests

#Sprawodzanie linku
def is_external(link: str, base: str) -> bool:
    link_domain = urlparse(link).netloc
    base_domain = urlparse(base).netloc
    return link_domain and link_domain != base_domain

def is_valid_url(url: str) -> bool:
    try:
        response = requests.head(url, allow_redirects=True, timeout=1.5)
        return response.status_code < 400
    except requests.RequestException:
        return False

def analyze(html: str, url: str = "https://example.com") -> dict:
    soup = BeautifulSoup(html, "html.parser")
    all_links = soup.find_all("a", href=True)

    external_links = []     
    valid_links = []         

    for tag in all_links:
        href = tag["href"]
        full_url = urljoin(url, href)  
        if is_external(full_url, url):
            external_links.append(full_url)
            if is_valid_url(full_url):
                valid_links.append(full_url)


    score = 100 if len(valid_links) >= 2 else 0

    return {
        "score": score,
        "external_links_found": len(external_links),
        "valid_external_links": len(valid_links),
        "valid_urls": valid_links[:5]  
    }
