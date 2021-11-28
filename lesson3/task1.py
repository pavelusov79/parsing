from bs4 import BeautifulSoup
import requests
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def search_vacancies():
    client = MongoClient('127.0.0.1', 27017)
    db = client['hh_db']
    vacancies = db.vacancies
    vacancies.create_index([('название вакансии', 1), ('компания', -1)])
    vacancy_name = input('Введите название вакансии, которую хотите найти: ').lower().replace(' ', '+')
    url = f'https://vladivostok.hh.ru/search/vacancy?text={vacancy_name}&area=1&fromSearchLine=true&items_on_page=20'
    headers = {'User-agent': 'Mozila/5.0'}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        pages = []
        soup = BeautifulSoup(res.text, 'lxml')
        next_pages = soup.find_all('a', attrs={'data-qa': 'pager-page'})
        if next_pages:
            for i in range(len(next_pages)):
               pages.append(int(next_pages[i].text))
        sum = 0 
        for i in range(pages[-1]):
            url = f'https://vladivostok.hh.ru/search/vacancy?text={vacancy_name}&area=1&fromSearchLine=true&items_on_page=20&page={i}'
            headers = {'User-agent': 'Mozila/5.0'}
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, 'lxml')
            parsed_names = soup.find_all('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})
            parsed_companies = soup.find_all('div', attrs={'class': 'vacancy-serp-item__meta-info-company'})
            parsed_cities = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'})
            parsed_data = soup.find_all('span', attrs={'class': 'vacancy-serp-item__publication-date vacancy-serp-item__publication-date_long'})
            for item in range(len(parsed_names)):
                parsed_item = {}
                parsed_item['_id'] = sum + item + 1
                parsed_item['название вакансии'] = parsed_names[item].text
                parsed_item['ссылка на вакансию'] = parsed_names[item]["href"]
                try:
                    salary = parsed_names[item].parent.parent.parent.parent.next_sibling.text.split()
                    if salary[0] == 'от':
                        parsed_item['мин зарплата'] = int("".join(salary[1:-1]))
                        parsed_item['макс зарплата'] = 'не указана'
                        parsed_item['валюта'] = salary[-1]
                    elif salary[0] == 'до':
                        parsed_item['мин зарплата'] = 'не указана'
                        parsed_item['макс зарплата'] = int("".join(salary[1:-1]))
                        parsed_item['валюта'] = salary[-1]
                    else:
                        parsed_item['мин зарплата'] = int("".join(salary[0:2]))
                        parsed_item['макс зарплата'] = int("".join(salary[3:-1]))
                        parsed_item['валюта'] = salary[-1]
                except Exception:
                    parsed_item['мин зарплата'] = 'не указана'
                    parsed_item['макс зарплата'] = 'не указана'
                    parsed_item['валюта'] = 'не указана'
                parsed_item['компания'] = parsed_companies[item].text
                parsed_item['город'] = parsed_cities[item].text
                parsed_item['дата публикации'] = parsed_data[item].text
                try:
                    vacancies.insert_one(parsed_item)
                except DuplicateKeyError:
                    pass
            sum += len(parsed_names)
            
            
           
search_vacancies()

