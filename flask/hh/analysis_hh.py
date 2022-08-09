import random
import requests
import json
import time
from tqdm import tqdm


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
    try:
        skills = data_two['key_skills']
        if skills:
            counter_skill += 1
            for skill in skills:
                if skill['name'] in requirements:
                    data_skills[skill['name']] += 1
                else:
                    data_skills[skill['name']] = 1
    except KeyError:
        pass
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
                                result[' '.join(name)] = data_two[key_word][
                                    word_dict]

    return result


def get_id_area(region, regions):
    region = region.lower()
    for places in regions:
        if region == places['name'].lower():
            return int(places['id'])
        for place in places['areas']:
            if region == place['name'].lower():
                return int(place['id'])
    return 11


if __name__ == '__main__':
    params_file = 'params.json'
    info_file = 'info.json'
    result_file = 'database.csv'
    request_address = f'https://api.hh.ru/vacancies'
    page = 0
    with open(params_file, 'r') as get_params:
        data_params = json.load(get_params)
    params = {
        'area': 113,
        'page': page
    }
    areas_address = f'https://api.hh.ru/areas/'
    id_areas = requests.get(areas_address).json()[0]['areas']
    id_1 = get_id_area(data_params['area'], id_areas)

    if data_params.get('text'):
        params['text'] = data_params['text']
    if data_params.get('area'):
        params['area'] = get_id_area(data_params['area'], id_areas)
    if data_params.get('employment'):
        params['employment'] = data_params['employment']
    if data_params.get('schedule'):
        params['schedule'] = data_params['schedule']

    average_salary = []  # Зарплата по каждому запросу
    requirements = {}  # Требования, списком
    vacancies_one = {}
    vacancies_two = {}

    counter_vacancies = 0
    counter_skill_vacancies = 0
    counter_salary_vacancies = 0
    columns = ["snippet", "id", "alternate_url", "employer",
               "schedule", "description", "name", "experience",
               "employment", "salary", "key_skills",
               "professional_roles", "address"]
    df = []
    # pages = requests.get(request_address, params=params).json()['pages']
    pages = 1
    for page in tqdm(range(pages)):
        params['page'] = page
        next_page = requests.get(request_address, params=params).json()
        for data_job in next_page['items']:
            time.sleep(1 + random.random())
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

    counter_vacancies = len(vacancies_one)
    dict_results = {}

    for i in tqdm(range(counter_vacancies)):
        data_job = vacancies_one[f'{i}']
        data_further = vacancies_two[f'{i}']
        counter_salary_vacancies, average_salary = salary_to_info(
            data_job, counter_salary_vacancies, average_salary)
        counter_skill_vacancies, requirements = skill_to_info(
            data_further, counter_skill_vacancies, requirements)
        dict_result = job_to_pandas(data_job, data_further)
        dict_results[i] = dict_result
        df.append(dict_result)

    # df_hh = pd.DataFrame(df)
    # df_hh.to_csv('database.csv')
    with open('database.json', 'w') as database:
        json.dump(dict_results, database)

    sorted_requirements = dict(sorted(requirements.items(),
                                      key=lambda item: item[1],
                                      reverse=True))
    # Сохраняем итоговую информацию
    result_info = dict()
    result_info['0'] = f'Дата обработки - {time.asctime()}'
    result_info['1'] = f'Всего вакансий обработано - {counter_vacancies}'
    result_info['2'] = f'Средняя заработная плата по вакансиям ' \
                       f'где она указана' \
             f' - {round(sum(average_salary) / counter_salary_vacancies)}' \
                       f' рублей'
    result_info['3'] = ['Требования', 'Кол-во раз', '%']

    for i, key in enumerate(sorted_requirements):
        interest = (sorted_requirements[
                        key] / counter_skill_vacancies * 100)
        round_interest = round(interest, 2)
        result_info[f'{i + 4}'] = [key, requirements[key], round(interest, 2)]
        if round_interest < 3.1:
            break

    with open('info.json', 'w') as info:
        json.dump(result_info, info)
