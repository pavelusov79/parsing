from pprint import pprint
from pymongo import MongoClient


def print_vacancies(salary, currency):
    client = MongoClient('127.0.0.1', 27017)
    db = client['hh_db']

    for el in db.vacancies.find({'мин зарплата': {'$gte': salary}, 'валюта': currency}):
        if not el:
            print(f'vacancy with search criteria: min salary = {salary} {currency} not found')
        else:
            pprint(el, sort_dicts=False)
    

print_vacancies(3000, 'USD')



