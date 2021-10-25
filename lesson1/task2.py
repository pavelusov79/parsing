import requests
import os
import json
import datetime


API_KEY = 'pnMogtyi6iLsxxCcVJjfUVdtrWayI3y50bNCw0TR'


def get_data_article_from_nasa(date):
    req = requests.get(f'https://api.nasa.gov/planetary/apod/?api_key={API_KEY}&date={date}')
    res = json.loads(req.text)
    path = os.path.join(os.getcwd(), 'task2.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f'Статья с "nasa api" за {datetime.datetime.strptime(res["date"], "%Y-%m-%d").strftime("%d.%m.%y")}\n')
        f.write(f"Автор:{res['copyright']}\nНазвание статьи: {res['title']}\nФото к статье: {res['url']}")


get_data_article_from_nasa('2021-10-20')






