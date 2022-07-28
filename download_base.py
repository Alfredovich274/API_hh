import requests
import json


if __name__ == '__main__':
    number = 0
    request_address = f'https://api.hh.ru/vacancies'
    page = 0
    params = {
        'text': '(машинн* AND обучен*) OR нейросет* OR python OR Python',
        'area': 2,
        'page': page
    }
    not_full_vacancy = {}
    full_vacancy = {}
    data = requests.get(request_address, params=params)
    print(data.status_code)
    pages = data.json()['pages']
    for page in range(pages):
        params['page'] = page
        data = requests.get(request_address, params=params).json()
        for vacancy in data['items']:
            not_full_vacancy[str(number)] = vacancy
            id_vacancy = vacancy['id']
            id_address = f'https://api.hh.ru/vacancies/{id_vacancy}'
            full_vacancy[str(number)] = requests.get(id_address).json()
            number += 1

    with open('not_full_vacancy.json', 'w') as not_full:
        json.dump(not_full_vacancy, not_full)

    with open('full_vacancy.json', 'w') as full:
        json.dump(full_vacancy, full)

    # Проверка читаемости файлов
    with open('not_full_vacancy.json', 'r') as not_full:
        not_full_file = json.load(not_full)

    print(type(not_full_file))

    with open('full_vacancy.json', 'r') as full:
        full_file = json.load(full)

    print(type(full_file))
