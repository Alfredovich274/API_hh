import requests


DOMAIN = 'https://www.100bestbooks.ru'

if __name__ == '__main__':

    page_1 = f'{DOMAIN}/index.php?page=1'
    requests_page_1 = requests.get(page_1)
    print('requests_page_1 - ', requests_page_1.status_code)
    with open('page_1.txt', 'w') as page:
        page.write(requests_page_1.text)

    url_book = 'https://www.100bestbooks.ru/item_info.php?id=12'
    requests_book = requests.get(url_book)
    print('requests_book - ', requests_book.status_code)
    with open('book_1.txt', 'w') as book:
        book.write(requests_book.text)
