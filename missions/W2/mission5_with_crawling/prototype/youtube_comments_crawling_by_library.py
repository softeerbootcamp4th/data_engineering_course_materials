from youtube_comment_downloader import *
import csv
import pandas as pd
from textblob import TextBlob

URL = 'https://www.youtube.com/watch?v=psbX7GAu6gM&ab_channel=carwow'
CAR_TYPE = 'i30'

if __name__=="__main__":
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(URL, sort_by=SORT_BY_RECENT)
    cids = []
    texts = []
    authors = []
    channel = []
    votes = []
    reply = []
    time_parsed = []
    sentiments = []

    for i, comment in enumerate(comments):
        cids.append(comment['cid'])
        texts.append(comment['text'])
        authors.append(comment['author'])
        channel.append(comment['channel'])
        votes.append(comment['votes'])
        reply.append(comment['reply'])
        sentiments.append(TextBlob(comment['text']).sentiment.polarity)
        time_parsed.append(comment['time_parsed'])
    
    file_path = f'{CAR_TYPE}_review_data.csv'
    data = pd.DataFrame({'cid': cids,
                        'text': texts,
                        'author': authors,
                        'channel': channel,
                        'votes': votes,
                        'reply': reply,
                        'time_parsed': time_parsed,
                        'sentiment': sentiments,
                        })

    data = data.drop_duplicates('text')
    data.to_csv(file_path, index=False)