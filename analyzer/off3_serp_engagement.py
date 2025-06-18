import random
def analyze() -> dict:
    # Symulacja współczynnika CTR lub bounce rate
    ctr = random.uniform(0.1, 0.8)  # CTR np. 10–80%
    score = 100 if ctr >= 0.4 else 50 if ctr >= 0.2 else 0

    return {
        "score": score,
        "simulated_ctr": round(ctr, 2),
        "note": "Demo – wymaga danych z Google Search Console"
    }
