from bs4 import BeautifulSoup
import requests
import os
import datetime


def search_vacancies():
    data = datetime.datetime.now().strftime('%d.%m.%Y_%H:%M')
    vacancy_name = input('Введите название вакансии, которую хотите найти: ').lower().replace(' ', '+')
    url = f'https://vladivostok.hh.ru/search/vacancy?text={vacancy_name}&area=1&fromSearchLine=true'
    headers = {'User-agent': 'Mozila/5.0'}
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        pages = []
        soup = BeautifulSoup(res.text, 'lxml')
        next_pages = soup.find_all('a', attrs={'data-qa': 'pager-page'})
        num = soup.find('h1', attrs={'data-qa': 'bloko-header-3'})
        if next_pages:
            for i in range(len(next_pages)):
               pages.append(int(next_pages[i].text))
        
        path = os.path.join(os.getcwd(), f'{data}_vacancies.txt')
        
        with open(path, 'w', encoding='utf-8') as f:
            sum = 0 
            f.write(f'Поиск по ключевым словам: {vacancy_name}\n')
            f.write(f'Дата поиска: {data}\n')
            if num:
                f.write(f'найдено: {num.text.split()[0]} вакансий\n\n')
            for i in range(pages[-1]):
                url = f'https://vladivostok.hh.ru/search/vacancy?text={vacancy_name}&area=1&fromSearchLine=true&page={i}'
                headers = {'User-agent': 'Mozila/5.0'}
                res = requests.get(url, headers=headers)
                soup = BeautifulSoup(res.text, 'lxml')
                f.write(f'Страница №{i + 1}\n')
                f.write(f'{url}\n\n')
                parsed_names = soup.find_all('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})
                parsed_companies = soup.find_all('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'})
                parsed_cities = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'})
                parsed_data = soup.find_all('span', attrs={'class': 'vacancy-serp-item__publication-date vacancy-serp-item__publication-date_long'})
                for item in range(len(parsed_names)):
                    f.write(f'№{sum + item + 1}\nназвание вакансии: {parsed_names[item].text}\nссылка на вакансию: {parsed_names[item]["href"]}\n')
                    if parsed_names[item].parent.parent.parent.parent.next_sibling:
                        f.write(f'зарплата: {parsed_names[item].parent.parent.parent.parent.next_sibling.next.text}\n')
                    else:
                        f.write('зарплата: не указана\n')
                    f.write(f'компания: {parsed_companies[item].text}\nгород: {parsed_cities[item].text}\nдата публикации : {parsed_data[item].text}\n\n')
                    f.write('-'*50)
                    f.write('\n\n')
                sum += len(parsed_names)
           

search_vacancies()