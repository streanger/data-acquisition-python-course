import requests
from itertools import count

def parse_soup(soup):
    """parse quotes and authors from grid cells"""
    cells = soup.find_all('div', class_="grid-item qb clearfix bqQt")
    parsed_cells = []
    for cell_index, cell in enumerate(cells):
        quote = cell.find('div', {'style': "display: flex;justify-content: space-between"}).text.strip()
        author = cell.find('a', {'title': "view author"}).text
        parsed_cells.append((quote, author))
    return parsed_cells
    
# scrape all pages
base_url = 'https://www.brainyquote.com/topics/page-quotes_{index}'
total_quotes = []
for index in count(1):
    url = base_url.format(index=index)
    print(f'{index}) {url}')
    response = requests.get(url)
    if (index > 1) and response.history:
        # 301 response code; page is moved
        break
    soup = BeautifulSoup(response.text)
    parsed_quotes = parse_soup(soup)
    total_quotes.extend(parsed_quotes)
    print(f'    parsed: {len(parsed_cells)}')
    
# unique & pretty print
total_quotes = sorted(set(total_quotes), key=lambda x:x[1])
for index, (quote, author) in enumerate(total_quotes):
    print(f'{index+1}) {quote} - {author}')
    
    