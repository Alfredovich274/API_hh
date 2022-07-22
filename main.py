import requests
import pprint

"""
Ищем вакансии:
1. В Санкт-петербурге или по всему миру, если работа удаленно, раздельно;
2. Python разработчик, стажер или Junior, разработчик нейронных сетей,
 раздельно;
3. Собираем данные раздельно по типам вакансий (Python, Web or AI);
4. Собираем необходимые навыки и знания по вакансиям, а так-же требуемый опыт
 работы в зависимости от навыков;
5. Собираем в 2 файла, для Python и AI отдельно по условию ДЗ;
6. Один общий файл для дальнейшего анализа, если потребуется со всеми данными
 и ссылками на вакансии.
"""

if __name__ == '__main__':

    DOMAIN = 'https://api.hh.ru/'  # https://spb.hh.ru/
    area_id = 2  # Санкт-Петербург
    # Ссылка для поиска региона
    # request_address = f'{DOMAIN}areas/{area_id}?additional_case=prepositional'
    request_address = f'{DOMAIN}vacancies'
    request_params = {
        'text': 'python AND junior',
        'area': 2,
        'page': 0
    }
    result = requests.get(request_address, params=request_params)

    # pprint.pprint(result.json()['items'])

    for items in result.json()['items']:
        # pprint.pprint(items)
        # print(type(items), len(items))
        # for i in items:
            # print(i)
        print(items['name'], items['area'])
        # break
