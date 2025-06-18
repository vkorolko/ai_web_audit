import random
def analyze() -> dict:
    shares = random.randint(0, 300)

    score = 100 if shares >= 100 else 50 if shares >= 20 else 0
    return {
        "score": score,
        "simulated_social_shares": shares
    }
