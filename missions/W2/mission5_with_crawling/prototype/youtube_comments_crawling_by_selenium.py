
import pandas as pd
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from textblob import TextBlob

CAR_TYPE = 'i30'
URL = "https://www.youtube.com/watch?v=psbX7GAu6gM&ab_channel=carwow"

def scroll(driver, scroll_time, wait_time):
    last_page_height = driver.execute_script(
        "return document.documentElement.scrollHeight"
    )
    stand_height = 0
    sub_height = last_page_height
    while True:
        current_height = driver.execute_script(
            "return document.documentElement.scrollHeight"
        )

        for i in range(10):
            driver.execute_script(
                f"window.scrollTo(0, {stand_height + (sub_height/10 * i)});"
            )
            time.sleep(scroll_time)
        time.sleep(wait_time)

        new_page_height = driver.execute_script(
            "return document.documentElement.scrollHeight"
        )
        stand_height = last_page_height
        sub_height = new_page_height - last_page_height
        if new_page_height == last_page_height:
            break
        last_page_height = new_page_height
        time.sleep(wait_time)
    return
    
    
def get_id(str_tmp):
    str_tmp = str_tmp.replace("@", "")
    str_tmp = str_tmp.strip()
    return str_tmp


def get_comment(str_tmp):
    str_tmp = str_tmp.replace("\n", " ")
    str_tmp = str_tmp.replace("\t", " ")
    str_tmp = str_tmp.replace("                ", " ")
    str_tmp = str_tmp.strip()
    return str_tmp

        
if __name__=="__main__":
    driver = webdriver.Chrome()
    driver.get(URL)

    time.sleep(3)

    # 스크롤링
    scroll(driver, 0.2, 1.5)

    time.sleep(2)

    req = driver.page_source
    soup = BeautifulSoup(req, "lxml")
    
    youtube_title = soup.find(
        "yt-formatted-string", class_="style-scope ytd-video-primary-info-renderer"
    ).text
    
    youtube_comments_IDs = soup.select("#author-text > span")
    youtube_comments = soup.select("#content-text > span")
    
    user_id_lst = []
    comments_lst = []
    sentiment_lst = []

    for user_id in youtube_comments_IDs:
        user_id_lst.append(get_id(user_id.get_text()))
        
    for comment in youtube_comments:
        comment = get_comment(comment.get_text())
        comments_lst.append(comment)
        blob = TextBlob(comment)
        sentiment_lst.append(blob.sentiment.polarity)
        
    file_path = f'{CAR_TYPE}_review_data_selenium.csv'
    data = pd.DataFrame({'ID': user_id_lst,
                        'text': comments_lst,
                        'sentiment': sentiment_lst})
    data.to_csv(file_path, index=False)