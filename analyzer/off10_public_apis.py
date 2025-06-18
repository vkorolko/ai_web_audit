import random
def analyze() -> dict:
    found = random.choice([True, False])
    score = 100 if found else 0

    return {
        "score": score,
        "api_documentation_found": found,
        "note": "Demo – można integrować z Swagger lub Postman API"
    }
