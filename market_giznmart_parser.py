import random
import re
import json
import requests
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


driver = webdriver.Firefox()


def get_product(url, category):
    driver.get(url)
    time.sleep(7)

    product = {}

    try:
        product_weight = driver.find_element(By.XPATH, "//div[@class='product-popup-info__weight']").text
        product_qual = re.findall(r'\d+', product_weight)
        product_qual = [int(i) for i in product_qual]

        product['name'] = driver.find_element(By.XPATH, "//div[@class='product-popup-info__title']").text
        product['category'] = category
        product['shop'] = 'Жизньмарт'
        product['weight'] = product_qual[0]
        product['price'] = int(re.findall(r'\d+', driver.find_element(By.XPATH, "//button[@class='product-actions__price']").text)[0])
        product['amount'] = product_qual[1]
        product['compound'] = driver.find_element(By.XPATH, "//div[@class='consist']").text
        product['description'] = driver.find_element(By.XPATH, "//div[@class='consist']").text
        product['cover'] = driver.find_element(By.XPATH, "//img[@class='product-popup-img__img']").get_attribute('src')

        bju_button = driver.find_elements(By.XPATH, "//button[contains(@class, 'product-popup-description__button')]")[1]
        bju_button.click()
        time.sleep(2)

        bju_table = driver.find_element(By.XPATH, "//div[@class='table-wrapper-bju']")
        bju = [float(bju_el.text.replace(',', '.')) for bju_el in bju_table.find_elements(By.XPATH, "//td")[-4:]]
        product['calories'] = bju[0]
        product['protein'] = bju[1]
        product['fats'] = bju[2]
        product['carbohydrates'] = bju[3]

    except:
        return None

    print(product)

    return product


def get_category_products(id, name, url):
    driver.get(url)
    time.sleep(2)

    category_products = []
    products_urls = [product_url.get_attribute('href') for product_url in driver.find_elements(By.XPATH, f"//div[@id='category_id-{id}']//a[@class='product__img-link']")]

    for product_url in products_urls:
        time.sleep(3)
        product = get_product(product_url, name)

        if product:
            category_products.append(product)

    return category_products


def create_category_products_api(data):
    create_product = requests.post('https://market.inverse-team.store/api/products/generate/', json=data)

    try:
        return json.dumps(create_product.json(), indent=4, ensure_ascii=False)
    except:
        return 'Nothing'


def get_categories_products(url):
    driver.get(url)

    time.sleep(4)
    select_city_button = driver.find_elements(By.XPATH, "//button[contains(@class, 'city-select-first-step__button')]")[0]
    select_city_button.click()
    time.sleep(4)

    select_address_button = driver.find_elements(By.XPATH, "//button[contains(@class, 'empty-delivery')]")[1]
    select_address_button.click()
    time.sleep(5)
    actions = ActionChains(driver)
    actions.move_by_offset(1000, 540).perform()
    time.sleep(4)
    actions.click().perform()

    time.sleep(4)
    admit_address_button = driver.find_element(By.XPATH, "//button[contains(@class, 'address-select__button')]")
    admit_address_button.click()

    time.sleep(7)
    close_button = driver.find_element(By.XPATH, "//button[@class='close-button']")
    close_button.click()

    time.sleep(5)

    categories = driver.find_elements(By.XPATH, "//a[contains(@class, 'top-line-categories__link')]")[1:]
    categories_urls = [[category.get_attribute('data-index'), category.text, category.get_attribute('href'), category] for category in categories]
    categories_products = {}

    time.sleep(2)

    for category in categories_urls:
        category_products = get_category_products(*category[:-1])

        if category_products:
            for category_product in category_products:
                if category_product:
                    print(create_category_products_api(category_product))

            categories_products[category[1]] = category_products

        print('---' * 20 + '>>>')
        time.sleep(6)

    driver.quit()

    return json.dumps(categories_products, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    print(get_categories_products('https://lifemart.ru/ekb/blyuda/'))