from bs4 import BeautifulSoup
from nltk.tokenize import PunktSentenceTokenizer, TreebankWordTokenizer

def analyze(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    headers = soup.find_all(["h1", "h2"])

    text = soup.get_text()
    sent_tokenizer = PunktSentenceTokenizer()
    word_tokenizer = TreebankWordTokenizer()
    sentences = sent_tokenizer.tokenize(text)
    words = []
    for sent in sentences:
        words.extend(word_tokenizer.tokenize(sent))

    total_words = len(words)

    qas_found = 0
    for header in headers:
        hdr_text = header.get_text(strip=True)
        if "?" in hdr_text:
            next_p = header.find_next_sibling()
            while next_p and next_p.name != "p":
                next_p = next_p.find_next_sibling()
            if next_p and len(next_p.get_text(strip=True)) > 30:
                qas_found += 1

    qas_expected = max(1, total_words // 500)
    score = min(1.0, qas_found / qas_expected) * 100

    return {
        "score": round(score, 2),
        "qas_found": qas_found,
        "qas_expected": qas_expected
    }
