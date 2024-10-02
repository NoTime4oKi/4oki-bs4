# import requests
# from bs4 import BeautifulSoup

# url = "https://www.atbmarket.com/catalog/economy/f/discount"

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
# }

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser')

#     catalog_list = soup.find('div', class_='catalog_list')

#     products = catalog_list.find_all('article', class_='catalog-item')

#     for product in products:
#         title_tag = product.find('div', class_='catalog-item__title wbh-28')
#         name = title_tag.find('a').text.strip() if title_tag else 'Без названия'

#         link = title_tag.find('a')['href'] if title_tag else '#'
#         full_link = f"https://www.atbmarket.com{link}"

#         price_tag = product.find('data', class_='product-price__top')
#         discount_price = price_tag.text.strip() if price_tag else 'Нет цены'

#         old_price_tag = product.find('data', class_='product-price__bottom')
#         old_price = old_price_tag.text.strip() if old_price_tag else 'Нет цены'

#         print(f"Name: {name}\nLink: {full_link}\nNew Price: {discount_price}\nOld Price: {old_price}")
#         print("-" * 40)
    
# else:
#     print(f"Не удалось получить доступ к сайту. Код ошибки: {response.status_code}")

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import re

def init_driver():
    options = Options()
    options.binary_location = 'C:/Program Files/Mozilla Firefox/firefox.exe'
    options.headless = True
    gecko_service = Service('geckodriver.exe')
    return webdriver.Firefox(service=gecko_service, options=options)

def parse_page(page_url):
    driver = init_driver()
    try:
        driver.get(page_url)
        time.sleep(5)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    finally:
        driver.quit()

base_url = "https://www.atbmarket.com/catalog/economy/f/discount"
for page in range(1, 6):  # Итерируемся по страницам 1-5
    url = f"{base_url}?page={page}"
    soup = parse_page(url)
    
    catalog_list = soup.find('div', class_='catalog-list')

    if catalog_list:
        print(f"Страница {page}")
        print("=" * 40)
        products = catalog_list.find_all('article', class_='catalog-item')

        for product in products:
            title_tag = product.find('div', class_=re.compile('catalog-item__title.*'))
            name = 'Без названия'
            full_link = '#'

            if title_tag:
                a_tag = title_tag.find('a')
                if a_tag:
                    name = a_tag.text.strip()
                    link = a_tag['href']
                    full_link = f"https://www.atbmarket.com{link}"

            price_tag = product.find('data', class_='product-price__top')
            discount_price = price_tag.text.strip() if price_tag else 'Нет цены'

            old_price_tag = product.find('data', class_='product-price__bottom')
            old_price = old_price_tag.text.strip() if old_price_tag else 'Нет цены'

            print(f"Название: {name}\nСсылка: {full_link}\nНовая цена: {discount_price}\nСтарая цена: {old_price}")
            print("-" * 40)
    else:
        print(f"Не удалось найти контейнер с товарами на странице {page}.")

