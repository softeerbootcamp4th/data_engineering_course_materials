import csv
import pandas as pd
from youtube_comment_downloader import *
from tqdm import tqdm
from textblob import TextBlob

from googletrans import Translator  
  
translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.co.kr',
    ])
translator.raise_Exception = True

CAR_URLS = { 
            'VELOSTER N':['https://www.youtube.com/watch?v=2DL7cAsCR6s&ab_channel=TheStraightPipes',
                          'https://www.youtube.com/watch?v=_zCaZFeAZU0&ab_channel=TheTopher'
                           ],
             'IONIQ 5 N':['https://www.youtube.com/watch?v=JVwfEOh0KBI&ab_channel=ThrottleHouse',
                          'https://www.youtube.com/watch?v=9ISB4MUubaM&ab_channel=TheStraightPipes',
                          ],
             'AVANTE N':['https://www.youtube.com/watch?v=sgpe7zuuCCU&ab_channel=ThrottleHouse',
                         'https://www.youtube.com/watch?v=Oy7d0jesePw&ab_channel=TheStraightPipes'
                         ],
             'i30N':['https://www.youtube.com/watch?v=psbX7GAu6gM&ab_channel=carwow',
                     'https://www.youtube.com/watch?v=4LZ6f6_0Dj4&ab_channel=CarExpert',
                    ],
}

FILE_PATH = f'Hyundai_N_comments.csv'

def text_transform(x):
    x = x.replace("\n", "")
    x = x.replace("\t", "")
    return x

def calc__sentiment(src_text):
    blob = TextBlob(src_text)
    sentiment = blob.sentiment.polarity
    return sentiment

if __name__=="__main__":
    car_type_lst = []
    texts = []
    sentiments = []

    for car_type, urls in tqdm(CAR_URLS.items()):
        for url in urls:
            downloader = YoutubeCommentDownloader()
            comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_RECENT)
            for i, comment in tqdm(enumerate(comments)):
                car_type_lst.append(car_type)
                text = comment['text'].replace("\n", "")
                texts.append(text)
                sentiment = calc__sentiment(text)
                sentiments.append(sentiment)
                # cids.append(comment['cid'])
                # authors.append(comment['author'])
                # channel.append(comment['channel'])
                # votes.append(comment['votes'])
                # reply.append(comment['reply'])
                # time_parsed.append(comment['time_parsed'])
    
    data = pd.DataFrame({
                        'car_type': car_type_lst,
                        'text': texts,
                        'sentiment': sentiments,
                        # 'cid': cids,
                        # 'author': authors,
                        # 'channel': channel,
                        # 'votes': votes,
                        # 'reply': reply,
                        # 'time_parsed': time_parsed,
                        })
    data.text = data.text.str.lower()
    data = data.drop_duplicates('text')
    data.to_csv(FILE_PATH, index=False)