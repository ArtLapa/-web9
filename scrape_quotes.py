import requests
from bs4 import BeautifulSoup
import json

def scrape_quotes(url):
    quotes_data = []
    authors_data = []

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Отримання інформації про цитати
        quotes = soup.select('div.quote')
        for quote in quotes:
            text = quote.select_one('span.text').text
            author = quote.select_one('small.author').text
            tags = [tag.text for tag in quote.select('div.tags a')]
            quotes_data.append({'text': text, 'author': author, 'tags': tags})

            # Отримання інформації про авторів
            if not any(a['name'] == author for a in authors_data):
                authors_data.append({'name': author, 'born': '', 'description': ''})

        # Перехід на наступну сторінку (якщо існує)
        next_page = soup.select_one('li.next a')
        url = next_page['href'] if next_page else None

    with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
        json.dump(quotes_data, quotes_file, ensure_ascii=False, indent=2)

    with open('authors.json', 'w', encoding='utf-8') as authors_file:
        json.dump(authors_data, authors_file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    quotes_url = 'http://quotes.toscrape.com'
    scrape_quotes(quotes_url)
