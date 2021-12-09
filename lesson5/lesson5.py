from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_urls():
    s = Service('/home/pavel/Downloads/geckodriver')
    global driver
    driver = Firefox(service=s)
    driver.get('https://mail.ru')
    username = driver.find_element(By.CLASS_NAME, 'email-input')
    username.send_keys('study.ai_172')
    click_next = driver.find_element(By.XPATH, '//button[@data-testid="enter-password"]')
    click_next.click()
    time.sleep(0.5)
    password = driver.find_element(By.CLASS_NAME, 'password-input')
    password.send_keys('NextPassword172#')
    click_next = driver.find_element(By.XPATH, '//button[@data-testid="login-to-mail"]')
    click_next.click()
    WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class, "js-letter-list-item")]')))
    urls = []
    while True:
        time.sleep(0.5)
        links = driver.find_elements(By.XPATH, '//a[contains(@class, "js-letter-list-item")]')
        href = links[-1].get_attribute('href')
        for link in links:
            urls.append(link.get_attribute("href"))
        links[-1].send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)
        new_links = driver.find_elements(By.XPATH, '//a[contains(@class, "js-letter-list-item")]')
        if new_links[-1].get_attribute("href") == href:
            break
    urls = list(set(urls))
    print(f'спарсено ccылок писем: {len(urls)}')
    return urls


def get_mail_info():
    client = MongoClient('127.0.0.1', 27017)
    db = client['lesson5_db']
    letters_collection = db['letters_collection']
    urls = get_urls()
    num = 1
    for url in urls:
        db_item = {}
        print(f'{num} - {url}')
        num +=1
        driver.get(url)
        name = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'thread__subject')))
        id = url.split(':')[2]
        from_el = driver.find_element(By.XPATH, '//span[@class="letter-contact"]').get_attribute('title')
        date_el = driver.find_element(By.CLASS_NAME, 'letter__date').text
        print(f'{id}\n{name.text}\n{from_el}\n{date_el}')
        db_item['_id'] = id
        db_item['Тема письма'] = name.text
        db_item['От кого'] = from_el
        db_item['Дата'] = date_el
        subj = driver.find_element(By.XPATH, '//div[contains(@class, "body-content")]').text
        print(subj)
        db_item['Текст письма'] = subj
        try:
            letters_collection.insert_one(db_item)
        except DuplicateKeyError:
            pass
        
    driver.close()
    print(f'занесено объектов в коллекцию БД: {letters_collection.estimated_document_count()}')    
    

get_mail_info()


