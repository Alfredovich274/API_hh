import json
import random


def calcul_salary(data):
    """
    Проверка наличия данных и выбор величины предлагаемой зарплаты.
    :param data: данные по зарплате со страницы вакансии - вакансия['salary'].
    :return: int, величина зарплаты в валюте указанной в вакансии.
    """
    return data['from'] if data['from'] and data['from'] > 0 else data['to']


def format_key_skills(full_data):
    """
    Преобразование списка словарей в строку требований через запятую.
    :param full_data: данные по требованиям
     со страницы вакансии - вакансия['key_skills'].
    :return: Строка со списком требований через запятую.
    """
    return ', '.join(val['name'] for val in full_data['key_skills'])


if __name__ == '__main__':
    key_description = {'id': 'код вакансии',
                       'snippet': '[requirement] - ключевые требования',
                       'alternate_url': 'ссылка на страницу вакансии',
                       'employer': '[name] - название компании',
                       'schedule': '[name] - график работы',
                       'description': 'чем занимается компания',
                       'name': 'название вакансии',
                       'experience': 'требуемый опыт',
                       'employment': '[name] - график работы (пример - полный'
                                     ' рабочий день)',
                       'salary': '[from] - величина зарплаты от, [to] - '
                                 'величина зарплаты до, [currency] - валюта',
                       'key_skills': 'ключевое навыки - список словарей',
                       'professional_roles': '[name]',
                       'address': '[raw] - адрес компании'
                       }

    keys_vacancy = ('id', 'snippet', 'alternate_url', 'employer', 'schedule',
                    'description', 'name', 'experience', 'employment', 'salary',
                    'key_skills', 'professional_roles', 'address')
    words_for_dict = ['requirement', 'name', 'raw', 'responsibility']
    words_for_salary = ['from', 'to', 'currency']
    files = ['not_full_vacancy.json', 'full_vacancy.json']
    print('{:<25}'.format('Ключи словаря по файлам'), end='')
    for name_file in files:
        print('{:^20}'.format(f'{name_file}'), end='')

    with open(files[0], 'r') as one_file:
        datafile_no_full = json.load(one_file)

    with open(files[1], 'r') as two_file:
        datafile_full = json.load(two_file)

    amount = len(datafile_no_full)
    number_vacancy = str(random.randint(0, amount))
    vacancy_no_full = datafile_no_full[number_vacancy]
    vacancy_full = datafile_full[number_vacancy]
    vacancies = [vacancy_no_full, vacancy_full]

    print('{:^90}'.format('Описание'))
    for key in keys_vacancy:
        print('{:<25}'.format(f'{key}'), end='')
        for vacancy in vacancies:
            print('{:^20}'.format('Ok') if key in vacancy else
                  '{:^20}'.format('--'), end='')
        print('   ', '{:<90}'.format(f'{key_description[key]}'))
    print(f'Рассмотрена вакансия № {number_vacancy}. '
          f' Ссылка на вакансию - {vacancy_no_full["alternate_url"]}')
    print(f'Вакансия - {vacancy_full["professional_roles"][0]["name"]}, '
          f'{vacancy_full["name"]}')
    print('Список ключевых требований к соискателю: ', end='')
    print(format_key_skills(vacancy_full))
    salary = 0
    fields_salary = vacancy_no_full['salary']
    if fields_salary:
        if fields_salary['currency'] and fields_salary['currency'] == 'RUR':
            salary = calcul_salary(fields_salary)
        else:
            salary = calcul_salary(fields_salary) * 60
    print(f'Предлагаемая зарплата - {salary}')
    print(f'Всего найдено {amount} вакансий.')
