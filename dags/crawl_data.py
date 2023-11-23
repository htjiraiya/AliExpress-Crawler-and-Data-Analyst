from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import chromedriver_autoinstaller
import json
import re
import os
from datetime import datetime

# pip install selenium chromedriver_autoinstaller dotenv azure-storage-blob apache-airflow


def safe_execute(default, exception, function, *args):
    try:
        if args[-1] == 'EYoOU':
            return len(function(*args))
        return function(*args).text
    except exception:
        return default


def get_products_info(e):
    link = e.find_element(By.CLASS_NAME, '_1UZxx').get_attribute('href')
    name = safe_execute(None, NoSuchElementException,
                        e.find_element, By.CLASS_NAME, 'nXeOv')
    sold = safe_execute(None, NoSuchElementException,
                        e.find_element, By.CLASS_NAME, 'Ktbl2')
    sold = re.findall(r'\d+', sold)[0]
    price = safe_execute(None, NoSuchElementException,
                         e.find_element, By.CLASS_NAME, 'U-S0j')
    promotion = safe_execute(None, NoSuchElementException,
                             e.find_element, By.CSS_SELECTOR, '_1BSEX._3dc7w._1jUmO')
    shipping = safe_execute(None, NoSuchElementException,
                            e.find_element, By.CLASS_NAME, '_3vRdz')
    feedback = safe_execute(None, NoSuchElementException,
                            e.find_elements, By.CLASS_NAME, 'EYoOU')

    product = {
        'name': name,
        'sold': sold,
        'price': price,
        'promotion': promotion,
        'shipping': shipping,
        'feedback': feedback,
        'link': link
    }
    return product


def main():
    chromedriver_autoinstaller.install()

    driver = webdriver.Chrome()
    driver.get("https://www.aliexpress.us/")
    wait = WebDriverWait(driver, 1)

    for i in range(10):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        try:
            see_more_btn = wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'pc2023-more-to-love--view-more-text--3aicjV_')))
            see_more_btn.click()
            sleep(1)
        except Exception as e:
            print(e)

    product_elements = driver.find_elements(By.CLASS_NAME, '_2FypS')
    products = [get_products_info(e) for e in product_elements]

    now = datetime.now()
    now_format = now.strftime("%Y_%m_%d %H_%M_%S")
    file_name_product = f'products_{now_format}.json'

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    # Create the path to the output file
    file_name_product = os.path.join(parent_dir, 'data', file_name_product)
    with open(file_name_product, 'w', encoding='utf-8') as file:
        json.dump(products, file)
    driver.quit()


if __name__ == "__main__":
    main()
