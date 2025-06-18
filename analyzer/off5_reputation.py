import random
def analyze() -> dict:
    rating = round(random.uniform(2.0, 5.0), 1)

    score = 100 if rating >= 4.0 else 50 if rating >= 3.0 else 0
    return {
        "score": score,
        "simulated_rating": rating,
        "note": "Demo – integracja z Trustpilot API możliwa"
    }
