import requests
import json
import os


def save_git_repos(user_name):
    req = requests.get(f'https://api.github.com/users/{user_name}/repos')
    res = json.loads(req.text)
    path = os.path.join(os.getcwd(), 'task1.txt')
    with open(path, 'w', encoding='utf-8') as f:
        for i in res:
            f.write(i['git_url'])
            f.write('\n')


save_git_repos('pavelusov79')





