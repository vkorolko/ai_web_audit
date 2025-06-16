import extruct
from bs4 import BeautifulSoup
from w3lib.html import get_base_url
from urllib.parse import urlparse

def analyze(html: str, url: str = "https://example.com") -> dict:
    base_url = get_base_url(html, url)
    
    data = extruct.extract(
        html,
        base_url=base_url,
        syntaxes=["json-ld"],
        uniform=True
    )

    jsonld_blocks = data.get("json-ld", [])
    valid_types = {"FAQPage", "HowTo", "Article", "QAPage"}
    valid_count = 0

    for item in jsonld_blocks:
        item_type = item.get("@type")
        if isinstance(item_type, list):
            if any(t in valid_types for t in item_type):
                valid_count += 1
        elif item_type in valid_types:
            valid_count += 1

    needed_blocks = 1 
    score = min(1.0, valid_count / needed_blocks) * 100

    return {
        "score": round(score, 2),
        "valid_jsonld": valid_count,
        "expected": needed_blocks
    }
