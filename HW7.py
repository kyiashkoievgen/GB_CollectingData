from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pymongo import MongoClient
import time

s = Service('chromedriver.exe')
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(service=s, options=options)

client = MongoClient('localhost:27017')
DB_collection = client['avito'].GeForce1080ti

driver.get('https://www.avito.ru/')

driver.implicitly_wait(60)
find = driver.find_element(By.XPATH, '//input')
find.send_keys('GeForce GTX 1080 Ti')
find.send_keys(Keys.ENTER)
wait = WebDriverWait(driver, 60)
wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"След")]')))
while 1:
    AD = {}
    for el in driver.find_elements(By.XPATH, '//meta[@itemprop="price"]'):
        main_div = el.find_element(By.XPATH, './../../../../../../div')
        AD = {
            'name': el.find_element(By.XPATH, './../../../../div/a/h3').text,
            'link': el.find_element(By.XPATH, './../../../../div/a').get_attribute('href'),
            'img': main_div.find_element(By.XPATH, './/img').get_attribute('src'),
            'price': el.get_attribute('content')
        }
        DB_collection.insert_one(AD)
    time.sleep(3)
    wait = WebDriverWait(driver, 60)
    next_btn = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(),"След")]')))
    next_btn[0].click()
