from itertools import count

import lxml
import requests
from bs4 import BeautifulSoup
from rich import print

RATING_MAPPING = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
}

def extract_direct_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    articles = soup.find_all('article', class_="product_pod")
    direct_urls = [f"{url}/{tag.a['href']}" for tag in articles]
    return direct_urls

def parse_direct_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    table = soup.find('table', {'class': "table table-striped"})
    rows = table.find_all('tr')
    values = {row.th.text:row.td.text for row in rows}
    rating_word = soup.find('p', {'class': 'star-rating'}).attrs['class'][1]
    values['rating'] = RATING_MAPPING[rating_word]
    return values

def mean_rating(values):
    """calculate mean rating"""
    total_rating = sum(item['rating'] for item in values)
    return round(total_rating/len(values), 1)

# scrape data
start_urls = [
    ('Philosophy', 'https://books.toscrape.com/catalogue/category/books/philosophy_7'),
    ('Music', 'https://books.toscrape.com/catalogue/category/books/music_14'),
    ('Autobiography', 'https://books.toscrape.com/catalogue/category/books/autobiography_27'),
]
parsed_data = {}
for index, (key, start_url) in enumerate(start_urls):
    print(f'{index+1}) {start_url}')
    direct_urls = extract_direct_urls(start_url)
    subvalues = [parse_direct_url(end_url) for end_url in direct_urls]
    parsed_data[key] = subvalues

# pretty print values
print(parsed_data)

# mean rating
mean = {key: mean_rating(values) for key, values in parsed_data.items()}
print(mean)
