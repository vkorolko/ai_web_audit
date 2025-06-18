import random
def analyze() -> dict:
    mentions = random.randint(0, 50)
    score = 100 if mentions >= 20 else 50 if mentions >= 5 else 0
    return {
        "score": score,
        "author_mentions": mentions
    }
