from bs4 import BeautifulSoup

def analyze(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    images = soup.find_all("img")

    total_images = len(images)
    alt_filled = sum(1 for img in images if img.get("alt") and img["alt"].strip())

    # warunek
    if total_images >= 5:
        ratio = alt_filled / total_images
        score = 100 if ratio >= 0.8 else 0
    else:
        score = 0

    return {
        "score": score,
        "total_images": total_images,
        "images_with_alt": alt_filled
    }
