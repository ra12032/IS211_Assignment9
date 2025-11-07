import requests
from bs4 import BeautifulSoup
import re

URL = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"

def clean(text):
    t = " ".join(text.replace("\xa0", " ").split())
    return t.replace("–", "-")

def main():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    table = None
    for t in soup.select("table.wikitable"):
        cap = t.find("caption")
        if cap and "Super Bowl championships" in cap.get_text():
            table = t
            break
    if not table:
        print("Could not find the Super Bowl champions table.")
        return

    for sup in table.select("sup"):
        sup.decompose()

    rows = table.select("tr")[1:]  # skip header

    print("\nSuper Bowl Champions:\n")
    count = 0
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        season = clean(cols[1].get_text(strip=True))
        winner = clean(cols[2].get_text(strip=True))
        score  = clean(cols[3].get_text(strip=True))
        loser  = clean(cols[4].get_text(strip=True))

        winner = re.sub(r"\s*\(\d+.*?\)$", "", winner)
        loser  = re.sub(r"\s*\(\d+.*?\)$", "", loser)

        count += 1
        print(f"{count}. Season: {season} | Winner: {winner} | Score: {score} | Loser: {loser}")
        if count == 20:
            break

if __name__ == "__main__":
    main()
