import requests
import time

def analyze(html: str = "", url: str = "https://example.com") -> dict:
    try:
        # Mierzymy czas ładowania za pomocą żądania GET
        start_time = time.time()
        response = requests.get(url, timeout=10)
        load_time = round(time.time() - start_time, 2)

        # Przyjmujemy, że jeśli strona ładuje się w ≤ 2.5 sekundy, to jest OK
        score = 100 if load_time <= 2.5 else 0

        return {
            "score": score,
            "load_time_seconds": load_time,
            "status_code": response.status_code
        }

    except requests.RequestException as e:
        return {
            "score": 0,
            "load_time_seconds": None,
            "error": str(e)
        }
