import collections
import multiprocessing
import os

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

collections.Callable = collections.abc.Callable


def scrape_pages(total_page, batch, i, company):
    # 크롬드라이버 실행
    driver = webdriver.Chrome()
    time.sleep(20)
    pages = total_page // batch
    for page in range(i * pages, i * pages + pages):
        scrape(driver, page, company)


def scrape(driver, page, company):
    # 크롬 드라이버에 url 주소 넣고 실행
    driver.get(
        f'https://www.indeed.com/cmp/{company}/reviews?fjobcat=manufacturing&fcountry=US&start={page * 20}')
    # 페이지가 완전히 로딩되도록 30초동안 기다림
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    reviews = soup.find("div", {"class": "cmp-ReviewsList"}).find_all("div", {"itemprop": "review"})
    rating = []
    title = []
    description = []
    for review in reviews:
        rating.append(float(review.find("div", {"itemprop": "reviewRating"}).text))
        title.append(review.find("h2", {"data-testid": "title"}).text)
        desc = []
        for row in review.find("span", {"itemprop": "reviewBody"}).find("span").find("span").find_all("span"):
            desc.append(row.text.replace("\r", ""))
        description.append(" ".join(desc))
    if not os.path.exists(f"./reviews/{company}"):
        os.makedirs(f"./reviews/{company}")
    pd.DataFrame({'title': title, 'description': description, 'rating': rating}).to_csv(
        f"./reviews/{company}/{page}.csv")

