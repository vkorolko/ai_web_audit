from bs4 import BeautifulSoup

def analyze(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    images = soup.find_all("img")
    videos = soup.find_all("video")
    iframes = soup.find_all("iframe")
    audio = soup.find_all("audio")

    total = len(images) + len(videos) + len(iframes) + len(audio)
    score = 100 if total > 0 else 0

    return {
        "score": score,
        "images": len(images),
        "videos": len(videos),
        "iframes": len(iframes),
        "audio": len(audio),
        "total_media_elements": total
    }
