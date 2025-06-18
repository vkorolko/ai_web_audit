import random
def analyze() -> dict:
    answers = random.randint(0, 10)
    score = 100 if answers >= 5 else 50 if answers >= 2 else 0

    return {
        "score": score,
        "simulated_expert_answers": answers
    }
