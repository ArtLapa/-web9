import requests
from bs4 import BeautifulSoup
import json

def get_author_dob(url):
    response_auth = requests.get(url)
    html_auth = response_auth.content
    auth_soup = BeautifulSoup(html_auth, "html.parser")
    auth_tag = auth_soup.find("span", class_="author-born-date")
    return auth_tag.text

def get_author_bplace(url):
    response_auth2 = requests.get(url)
    html_auth2 = response_auth2.content
    auth_soup2 = BeautifulSoup(html_auth2, "html.parser")
    auth_tag2 = auth_soup2.find("span", class_="author-born-location")
    return auth_tag2.text

url = "http://quotes.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
tags = soup.find_all("div", class_="quote")

authors_data = []
for t in tags:
    a = t.find("small", class_="author").text
    hrefs = t.a
    link = hrefs.get("href")
    link_url = url + link
    dob = get_author_dob(link_url)
    b_place = get_author_bplace(link_url)
    authors_data.append({"author": a, "dob": dob, "birthplace": b_place})

# Збереження у JSON-файл
with open("authors.json", "w") as authors_file:
    json.dump(authors_data, authors_file, indent=4)

print("Інформацію про авторів збережено у файлі authors.json")

