from itertools import count
import os
from pathlib import Path
import sys

import lxml
import requests
from bs4 import BeautifulSoup
from rich import print
import pandas as pd


def parse_otomoto_offer(url):
    """parse single offer values"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    params_items = soup.find_all('li', {'class': "offer-params__item"})
    parsed = {}
    for item in params_items:
        label = item.span.text
        value = item.div.text.strip()
        parsed[label] = value
    return parsed


def find_page_offers(url):
    """find offers on single page"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    main = soup.find('main', {'data-testid': "search-results"})
    articles = main.find_all('article')
    offers = [item.a['href'] for item in articles]
    return offers


def get_pagination_number(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")
    pagination_list = soup.find('ul', class_="pagination-list")
    pages_numbers = pagination_list.find_all('li')
    number = 0
    for item in reversed(pages_numbers):
        label = item.get('aria-label', False)
        if not label:
            continue
        if label.startswith('Page '):
            try:
                number = int(label.split()[-1])
                break
            except:
                continue
    if not number:
        raise ValueError('Pagination not parsed properly')
    return number


if __name__ == "__main__":
    # get pagination
    base_url = 'https://www.otomoto.pl/osobowe/seg-mini/od-2007?search%5Bfilter_float_mileage%3Afrom%5D=35000&search%5Bfilter_float_mileage%3Ato%5D=100000&search%5Bfilter_float_year%3Ato%5D=2012'
    pagination = get_pagination_number(base_url)
    print(f'{pagination=}')
    input('press enter to start ')

    # scrape data
    total_details = []
    for index in range(1, pagination+1):
        url = f'{base_url}&page={index}'
        print(f'{index}) {url}')
        offers = find_page_offers(url)
        print(f'    {len(offers)=}')
        details = list(map(parse_otomoto_offer, offers))
        total_details.extend(details)

    # save data
    os.chdir(str(Path(os.path.dirname(sys.argv[0])).parent))
    df = pd.DataFrame(total_details)
    df.index += 1
    out = 'otomoto.csv'
    df.to_csv(out)
    print(f'data saved to: {out}')
