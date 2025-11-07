import requests
from bs4 import BeautifulSoup

URL = "https://www.macrotrends.net/stocks/charts/AAPL/apple/stock-price-history"

def main():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    table = soup.select_one("table.table")
    if not table:
        print("Could not find the stock price table.")
        return

    rows = table.select("tbody tr")

    print("\nApple Stock Historical Closing Prices:\n")

    count = 0
    for row in rows:
        cols = row.find_all("td")
        # Table format: Date | Close | High | Low | Volume
        if len(cols) < 2:
            continue

        date = cols[0].get_text(strip=True)
        close = cols[1].get_text(strip=True)

        print(f"Date: {date} | Close: {close}")
        count += 1

        if count == 20:
            break

if __name__ == "__main__":
    main()
