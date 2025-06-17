import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from urllib.parse import urljoin

def analyze(html: str, page_url: str) -> int:
    wynik_sitemap = 0
    wynik_html_data = 0

    #<lastmod> z sitemap.xml
    sitemap_url = urljoin(page_url, "/sitemap.xml")
    try:
        resp = requests.get(sitemap_url, timeout=5)
        if resp.status_code == 200:
            sitemap_xml = resp.text
            lastmod_znalezione = re.findall(r"<lastmod>(.*?)</lastmod>", sitemap_xml)
            if lastmod_znalezione:
                najnowsza_data = max(parse_date(d) for d in lastmod_znalezione if parse_date(d))
                if najnowsza_data and is_recent(najnowsza_data, 90):
                    wynik_sitemap = 100
    except Exception as e:
        print(f"[OSTRZEŻENIE] Nie udało się pobrać sitemap.xml: {e}")

    #<time datetime="..."> z HTML
    try:
        soup = BeautifulSoup(html, "html.parser")
        time_tag = soup.find_all("time", datetime=True)
        for tag in time_tag:
            data_html = parse_date(tag.get("datetime"))
            if data_html and is_recent(data_html, 90):
                wynik_html_data = 100
                break
    except Exception as e:
        print(f"[OSTRZEŻENIE] Nie udało się przetworzyć tagu <time>: {e}")
    wynik_koncowy = round(0.7 * wynik_sitemap + 0.3 * wynik_html_data)
    return wynik_koncowy

def parse_date(data_str):
    try:
        return datetime.fromisoformat(data_str.strip().replace("Z", "+00:00"))
    except ValueError:
        try:
            return datetime.strptime(data_str.strip(), "%Y-%m-%d")
        except:
            return None

def is_recent(data: datetime, dni: int) -> bool:
    return (datetime.utcnow() - data) <= timedelta(days=dni)
