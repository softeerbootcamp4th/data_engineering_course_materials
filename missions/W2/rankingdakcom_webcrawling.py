import csv
import logging
import math
import re

import pandas as pd
from selenium import webdriver
from selenium.common import exceptions as SE
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm


NUM_TO_TRY = 100
REVIEWS_PER_PAGE = 5
RANKING_URL = 'https://www.rankingdak.com/display/rank/sale'
RESTART_PRODUCT_FROM = 32
RESTART_PAGE_FROM = 2


if __name__ == '__main__':
    logging.basicConfig(
    filename='rankingdakcom_webcrawling_log.txt',
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 3000)

    driver.get(RANKING_URL)
    driver.implicitly_wait(2)

    num_of_products = 0
    while num_of_products <= 0:
        num_of_products = len(wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, '//*[@id="div_rankList"]/ol/li')
        )))

    products = []

    for product_id in range(1, num_of_products + 1):
        product_name = wait.until(EC.presence_of_element_located(
            (By.XPATH, f'//*[@id="div_rankList"]/ol/li[{product_id}]/div/div/div[2]/p[1]/a')
        )).text
        product_url = wait.until(EC.presence_of_element_located(
            (By.XPATH, f'//*[@id="div_rankList"]/ol/li[{product_id}]/div/div/div[2]/p[1]/a')
        )).get_attribute('href')
        num_of_reviews = wait.until(EC.presence_of_element_located(
            (By.XPATH, f'//*[@id="div_rankList"]/ol/li[{product_id}]/div/div/div[4]/div/span[2]')
        )).text

        num_of_reviews = re.sub(r'[\(\),]', '', num_of_reviews)
        num_of_reviews = int(num_of_reviews)

        products.append([product_name, product_url, num_of_reviews])

    pd.DataFrame(products, columns=['product_name', 'product_url', 'num_of_reviews']).to_csv('product_ranking.csv')

    products = sorted(products, key=lambda x: x[2])[RESTART_PRODUCT_FROM:]
    
    for product_name, product_url, num_of_reviews in tqdm(products, desc='Product', position=0):
        driver.get(product_url)

        f = open('chicken_reviews/' + product_name + '.csv', 'w', newline='\n', encoding='utf-8')
        writer = csv.writer(f)
        writer.writerow(['rating', 'review'])
        
        max_page = min(math.ceil(num_of_reviews / REVIEWS_PER_PAGE), 3000 // REVIEWS_PER_PAGE)
        for page_i in tqdm(range(RESTART_PAGE_FROM, max_page + 1), position=1):
            if RESTART_PAGE_FROM > 2:
                RESTART_PAGE_FROM = 2

            wait.until(EC.presence_of_element_located(
                (By.XPATH, f'//*[@id="prodReviewList"]/div[2]/div/div/div')
            ))
            num_of_reviews_in_page = len(driver.find_elements(by=By.XPATH, value='//*[@id="prodReviewList"]/div[1]/ul/li'))
                
            for review_i in range(1, num_of_reviews_in_page + 1):
                while True:
                    try:
                        rating_elem = driver.find_element(by=By.XPATH, value=f'//*[@id="prodReviewList"]/div[1]/ul/li[{review_i}]/div/div[1]/div[1]/div/em/span[2]')
                        rating = rating_elem.text
                    except (TimeoutError, SE.StaleElementReferenceException):
                        logging.error('Failed to read rating in #%i review', review_i)
                    except SE.NoSuchElementException:
                        logging.error('Failed to find rating in #%i review', review_i)
                    except Exception as e:
                        logging.error('Stopping running %i product(next page: %i)', RESTART_PRODUCT_FROM, page_i)
                        raise e
                    else:
                        break

                while True:
                    try:
                        review_elem = driver.find_element(by=By.XPATH, value=f'//*[@id="prodReviewList"]/div[1]/ul/li[{review_i}]/div/div[1]/div[1]/p[2]/span')
                        review = review_elem.text.strip()
                    except (TimeoutError, SE.StaleElementReferenceException):
                        logging.error('Failed to read review in #%i page', page_i)
                    except SE.NoSuchElementException:
                        review_elem = driver.find_element(by=By.XPATH, value=f'//*[@id="prodReviewList"]/div[1]/ul/li[{review_i}]/div/div[1]/div[1]/p/span')
                        review = review_elem.text.strip()
                        break
                    except Exception as e:
                        logging.error('Stopping running %i product(next page: %i)', RESTART_PRODUCT_FROM, page_i)
                        raise e
                    else:
                        break

                rating = rating[2:]
                review = review.replace("BEST ", "").replace("\n", "\\n")
                writer.writerow([rating, review])

            if page_i < max_page:
                next_page = (page_i - 2) % 10 + 3

                while True:
                    try:
                        next_page_elem = driver.find_element(By.XPATH, f'//*[@id="prodReviewList"]/div[2]/div/div/div/a[{next_page}]')
                        next_page_elem.click()
                    except (TimeoutError, SE.StaleElementReferenceException):
                        logging.error('Failed to find next page %i', page_i)
                    except SE.ElementClickInterceptedException:
                        logging.error('Stopping running %i product(next page: %i)', RESTART_PRODUCT_FROM, page_i)
                    except Exception as e:
                        logging.error('Stopping running %i product(next page: %i)', RESTART_PRODUCT_FROM, page_i)
                        raise e
                    else:
                        break

        f.close()
        RESTART_PRODUCT_FROM += 1

    driver.quit()