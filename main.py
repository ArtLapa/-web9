import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            text = quote.css('span.text::text').get().strip()
            author = quote.css('small.author::text').get().strip()
            tags = quote.css('a.tag::text').getall()
            yield {
                'text': text,
                'author': author,
                'tags': tags
            }
            yield scrapy.Request(response.urljoin(quote.css('span a::attr(href)').get()), callback=self.parse_author)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response):
        yield {
            'name': response.css('h3.author-title::text').get().strip(),
            'born': response.css('span.author-born-date::text').get().strip(),
            'description': response.css('div.author-description::text').get().strip(),
        }

# Save data to JSON files
with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
    quotes_data = []
    with open('quotes.jl', 'r', encoding='utf-8') as f:
        for line in f:
            quotes_data.append(json.loads(line))
    json.dump(quotes_data, quotes_file, ensure_ascii=False, indent=2)

with open('authors.json', 'w', encoding='utf-8') as authors_file:
    authors_data = []
    with open('authors.jl', 'r', encoding='utf-8') as f:
        for line in f:
            authors_data.append(json.loads(line))
    json.dump(authors_data, authors_file, ensure_ascii=False, indent=2)

