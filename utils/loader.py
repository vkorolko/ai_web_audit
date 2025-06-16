# utils/loader.py

import requests

def fetch_html(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"[ERROR] HTTP {response.status_code} for {url}")
    except Exception as e:
        print(f"[EXCEPTION] {e}")
    return None
