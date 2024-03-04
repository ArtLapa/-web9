import requests
from bs4 import BeautifulSoup
import json

# URL сайту для скрапінгу
url = "http://quotes.toscrape.com"

# Отримання HTML-сторінки
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Збереження цитат у словник
quotes = []
for quote in soup.find_all("div", class_="quote"):
    text = quote.find("span", class_="text").text
    author = quote.find("small", class_="author").text
    tags = [tag.text for tag in quote.find_all("a", class_="tag")]
    quotes.append({"text": text, "author": author, "tags": tags})

# Збереження у JSON-файл
with open("quotes.json", "w") as quotes_file:
    json.dump(quotes, quotes_file, indent=4)

print("Цитати збережено у файлі quotes.json")
