import pprint
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import random
import json
from orm import add_line
import subprocess


def del_n(data):
    return data.replace('\n\n', ' ').replace('  ',
                                             ' ').replace('--', '-').lstrip()


DOMAIN = 'https://www.100bestbooks.ru'

if __name__ == '__main__':
    result_100 = {}
    page = 1
    pages = 1
    pages_bool = True
    counter = 0
    subprocess.run("python3 orm.py", shell=True)

    while page <= pages:
        # book_info = {}
        url_page = f'{DOMAIN}/index.php?page={page}'
        requests_page = requests.get(url_page)
        soup_domain = BeautifulSoup(requests_page.text, 'html.parser')
        # Определяем количество страниц
        if pages_bool:
            pages_bool = False
            pages_info = soup_domain.find_all('td', class_="table-bottom")
            for amount_pages in pages_info:
                if 'Страницы' in amount_pages.text:
                    amount_page = amount_pages.find_all('a')
                    # pages = int(amount_page[len(amount_page) - 1].text)
                    pages = 1
            print('Всего страниц', pages)
        page_books = soup_domain.find_all('tr', style="text-align: center")
        # pprint.pprint(page_books)
        # input()
        for one_book in tqdm(page_books):
            book_info = {}
            for i, data_book in enumerate(one_book):
                if i == 1:
                    variable = False
                    for n, tag in enumerate(data_book.find_all('a')):
                        book_info['author' if n == 0 else 'title'] = tag.text
                        if variable:
                            book_info['link'] = f"{DOMAIN}/{tag.get('href')}"
                        variable = True
                elif 1 < i <= 3:
                    book_info['year' if i == 2 else 'rating'] = data_book.text
            requests_book = requests.get(book_info['link'])
            soup_book = BeautifulSoup(requests_book.text, 'html.parser')
            description = soup_book.find('p', itemprop="description")
            if description:
                book_info['description'] = del_n(description.text)
            else:
                book_info['description'] = None
            citation = soup_book.find('span', itemprop="citation")
            if citation:
                book_info['citation'] = del_n(citation.text)
            else:
                book_info['citation'] = None
            for a in soup_book.find_all('a'):
                if 'Скачать' in str(a.get('title')):
                    book_info[f"link_{a.get('title')[-3:]}"] = f"{DOMAIN}/{a.get('href')}"

            result_100[str(counter)] = book_info
            add_line(book_info)
            counter += 1

        time.sleep(random.randint(1, 3))
        page += 1

    with open('100books.json', 'w') as log:
        json.dump(result_100, log)
