import requests
from bs4 import BeautifulSoup
import json

def get_author_info(url):
    response_auth = requests.get(url)
    html_auth = response_auth.content
    auth_soup = BeautifulSoup(html_auth, "html.parser")
    auth_tag = auth_soup.find("span", class_="author-born-date")
    dob = auth_tag.text.strip() if auth_tag else ""
    auth_location_tag = auth_soup.find("span", class_="author-born-location")
    location = auth_location_tag.text.strip() if auth_location_tag else ""
    return dob, location

url = "http://quotes.toscrape.com"
all_quotes = []

# Iterate through all pages
while url:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    quotes = soup.find_all("div", class_="quote")

    for quote in quotes:
        text = quote.find("span", class_="text").text.strip()
        author = quote.find("small", class_="author").text.strip()
        about_link = quote.find("a", href=True)["href"]
        author_url = url + about_link
        dob, location = get_author_info(author_url)

        all_quotes.append({
            "quote": text,
            "author": author,
            "dob": dob,
            "location": location
        })

    next_page = soup.find("li", class_="next")
    url = url + next_page.a["href"] if next_page else None

# Save quotes to JSON file
with open("quotes.json", "w") as quotes_file:
    json.dump(all_quotes, quotes_file, indent=4)

print("Цитати збережено у файлі quotes.json")

