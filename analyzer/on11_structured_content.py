from bs4 import BeautifulSoup

def analyze(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    #ustrukturyzowany elementy
    lists = soup.find_all(["ul", "ol"])
    tables = soup.find_all("table")
    blockquotes = soup.find_all("blockquote")
    icons = soup.find_all(class_="icon") 

    #lącznie
    structured_elements = len(lists) + len(tables) + len(blockquotes) + len(icons)

    score = 100 if structured_elements >= 2 else 0

    return {
        "score": score,
        "lists": len(lists),
        "tables": len(tables),
        "blockquotes": len(blockquotes),
        "icons": len(icons),
        "total_structured_elements": structured_elements
    }
