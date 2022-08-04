import os.path
import requests
import json
import time
from tqdm import tqdm
import pandas as pd


def treatment_str(data):
    """
    Убираем ненужные символы в строковых данных.
    :param data: Строка.
    :return: Строка.
    """
    deleted_words = ['<p>', '<strong>', '</p>', '</strong>', '<ul>', '<li>',
                     '</li>', '</ul>', '<highlighttext>', '</highlighttext>',
                     '\r', '\r\n', '<br />', '</ol>', '<ol>']
    for i_str in deleted_words:
        if isinstance(data, str):
            data = data.replace(i_str, '')
    return data


def calcul_salary(data):
    """
    Проверка наличия данных и выбор величины предлагаемой зарплаты.
    :param data: данные по зарплате со страницы вакансии - вакансия['salary'].
    :return: int, величина зарплаты в валюте указанной в вакансии.
    """
    return data['from'] if data['from'] and data['from'] > 0 else data['to']


def salary_to_info(data_one, counter_salary, avg_salary):
    """
    Готовим данные для отчета по зарплате.
    :param data_one: Не полное описание вакансии,
    полученное со страницы с вакансиями.
    :param counter_salary: Счетчик вакансий,
    где указаны предложения по зарплате.
    :param avg_salary: Список предложений
    по зарплате всех рассмотренных вакансий.
    :return: Возвращаем счетчик (int) и список зарплат (list).
    """
    data_salary = data_one['salary']
    if data_salary:
        if data_salary['currency'] and data_salary['currency'] == 'RUR':
            avg_salary.append(calcul_salary(data_salary))
            counter_salary += 1
        else:
            avg_salary.append(calcul_salary(data_salary) * 60)
            counter_salary += 1
    return counter_salary, avg_salary


def skill_to_info(data_two, counter_skill, data_skills):
    """
    Готовим данные для отчета по требованиям.
    :param data_two: Полное описание вакансии, полученное по запросу конкретной
    вакансии (по id).
    :param counter_skill: Счетчик вакансий, где указаны требования
    :param data_skills: Список словарей с требованиями: количество упоминаний.
    :return: Счетчик (int) и список словарей по требованиям.
    """
    # TODO добавить анализ 'snippet': '[requirement]
    skills = data_two['key_skills']
    if skills:
        counter_skill += 1
        for skill in skills:
            if skill['name'] in requirements:
                data_skills[skill['name']] += 1
            else:
                data_skills[skill['name']] = 1
    return counter_skill, data_skills


def job_to_pandas(data_one, data_two):
    """
    Формирование данных для формирования pandas данных
    для возможного дальнейшего анализа.
    :param data_one: Не полное описание вакансии,
    полученное со страницы с вакансиями.
    :param data_two: Полное описание вакансии, полученное по запросу конкретной
    вакансии (по id).
    :return: Список выборочных данных из вакансии.
    """
    keys_one = "snippet"
    keys_two = ("id", "alternate_url", "employer", "schedule",
                "description", "name", "experience", "employment", "salary",
                "key_skills", "professional_roles", "address")
    words_for_dict = ['requirement', 'name', 'raw', 'responsibility', 'from',
                      'to', 'currency']
    result = {}
    value_one = data_one[keys_one]
    data = ''
    for key_word in words_for_dict:
        if key_word in value_one:
            if value_one[key_word]:
                data += treatment_str(value_one[key_word])
    result[keys_one] = data
    for key_word in keys_two:
        if key_word in data_two:
            if data_two[key_word]:
                if isinstance(data_two[key_word], str):
                    result[key_word] = treatment_str(data_two[key_word])
                elif isinstance(data_two[key_word], list):
                    for value_list in data_two[key_word]:
                        for word in words_for_dict:
                            if word in value_list:
                                name = [key_word, word]
                                result[' '.join(name)] = value_list[word]
                elif isinstance(data_two[key_word], dict):
                    for word_dict in words_for_dict:
                        if word_dict in data_two[key_word]:
                            if data_two[key_word][word_dict]:
                                name = [key_word, word_dict]
                                result[' '.join(name)] = data_two[key_word][word_dict]

    return result


if __name__ == '__main__':
    files = ['python_hh.json', 'info.txt']
    request_address = f'https://api.hh.ru/vacancies'
    page = 0
    params = {
        'text': 'python developer',
        'area': 113,
        'page': page
    }
    average_salary = []  # Зарплата по каждому запросу
    requirements = {}  # Требования, списком
    vacancies_one = {}
    vacancies_two = {}
    print('Если парсинг, то - 1, \n'
          'Если парсинг произведен и необходимо обработать файлы, то - 2\n'
          'Выйти из программы, введите 0\n')
    menu = 99
    counter_vacancies = 0
    counter_skill_vacancies = 0
    counter_salary_vacancies = 0
    columns = ["snippet", "id", "alternate_url", "employer",
               "schedule", "description", "name", "experience",
               "employment", "salary", "key_skills",
               "professional_roles", "address"]
    df = []
    while menu:
        if menu != 'read info file':
            menu = int(input('Выбор? '))
        if menu == 1:
            pages = requests.get(request_address, params=params).json()['pages']
            print(f'Всего страниц - {pages}')

            for page in tqdm(range(pages)):
                params['page'] = page
                next_page = requests.get(request_address, params=params).json()
                for data_job in next_page['items']:
                    # Обработка одой вакансии
                    id_address = f'https://api.hh.ru/vacancies/{data_job["id"]}'
                    data_further = requests.get(id_address).json()
                    vacancies_one[str(counter_vacancies)] = data_job
                    vacancies_two[str(counter_vacancies)] = data_further
                    counter_salary_vacancies, average_salary = salary_to_info(
                        data_job, counter_salary_vacancies, average_salary)
                    counter_skill_vacancies, requirements = skill_to_info(
                        data_further, counter_skill_vacancies, requirements)
                    job_to_pandas(data_job, data_further)
                    counter_vacancies += 1
            print('Записываем файлы')
            with open('base_hh_one.json', 'w') as not_full:
                json.dump(vacancies_one, not_full)

            with open('base_hh_two.json', 'w') as full:
                json.dump(vacancies_two, full)
            menu = 'read info file'
            print('Отчет:')
        elif menu == 2:
            if not os.path.isfile('base_hh_one.json'):
                print('Файл base_hh_one.json не существует')
                break
            if not os.path.isfile('base_hh_two.json'):
                print('Файл base_hh_two.json не существует')
                break

            with open('base_hh_one.json', 'r') as not_full:
                database_one = json.load(not_full)
            if not database_one:
                print('Нет данных в файле base_hh_one.json')
                break
            with open('base_hh_two.json', 'r') as not_full:
                database_two = json.load(not_full)
            if not database_two:
                print('Нет данных в файле base_hh_two.json')
                break
            counter_vacancies = len(database_one)
            for i in tqdm(database_one):
                data_job = database_one[i]
                data_further = database_two[i]
                counter_salary_vacancies, average_salary = salary_to_info(
                    data_job, counter_salary_vacancies, average_salary)
                counter_skill_vacancies, requirements = skill_to_info(
                    data_further, counter_skill_vacancies, requirements)

                df.append(job_to_pandas(data_job, data_further))

            menu = 'read info file'
        elif menu == 'read info file':
            print('Сохраняем данные Pandas в database_hh.csv')
            df_hh = pd.DataFrame(df)
            print(df_hh.head())
            df_hh.to_csv('database_hh.csv')
            sorted_requirements = dict(sorted(requirements.items(),
                                              key=lambda item: item[1],
                                              reverse=True))
            with open('info_hh.txt', 'w') as info_file:
                line_1 = f'Дата обработки - {time.asctime()} \n'
                info_file.write(line_1)
                print(line_1, end='')
                line_2 = f'Всего вакансий обработано - {counter_vacancies}\n'
                info_file.write(line_2)
                print(line_2, end='')
                line_3 = f'Средняя заработная плата по вакансиям ' \
                         f'где она указана' \
                         f' - {round(sum(average_salary) / counter_salary_vacancies)}' \
                         f' рублей\n'
                info_file.write(line_3)
                print(line_3)
                line_4 = f'     Требования                         ' \
                         f'Кол-во раз    %\n'
                info_file.write(line_4)
                print(line_4)
                for key in sorted_requirements:
                    interest = (sorted_requirements[
                                    key] / counter_skill_vacancies * 100)
                    round_interest = round(interest, 2)
                    line_5 = f"{'{:<40}'.format(key)}" \
                             f"{'{:^10}'.format(requirements[key])}" \
                             f"{'{:^10}'.format(round_interest, 2)}\n"
                    info_file.write(line_5)
                    print(line_5, end='')
                    if round_interest < 3.1:
                        break
            menu = 0
        elif menu == 0:
            pass
        else:
            print('Нет такого варианта.')
