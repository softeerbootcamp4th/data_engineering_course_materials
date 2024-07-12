import pandas
import warnings 
from googleapiclient.discovery import build
from textblob import TextBlob

warnings.filterwarnings('ignore')

CAR_TYPE='i30'
API_KEY = 'AIzaSyB7v8vlf_3XcTjF0Eiq4Ii8E7Ckw7HR0GU'
VIDEO_ID = "EOCDIzUKRwc"
 
if __name__ == "__main__":
    comments = list()
    api_obj = build('youtube', 'v3', developerKey=API_KEY)
    response = api_obj.commentThreads().list(part='snippet,replies', videoId=VIDEO_ID, maxResults=100).execute() 

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append([comment['textDisplay'], comment['authorDisplayName'], comment['publishedAt'], comment['likeCount']])
            
            if item['snippet']['totalReplyCount'] > 0:
                for reply_item in item['replies']['comments']:
                    reply = reply_item['snippet']
                    comments.append([reply['textDisplay'], reply['authorDisplayName'], reply['publishedAt'], reply['likeCount']])
                    
        if 'nextPageToken' in response:
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=VIDEO_ID, pageToken=response['nextPageToken'], maxResults=100).execute()
        else:
            break
        
    df = pandas.DataFrame(comments)
    df.columns=['text', 'ID', 'PublishedAt', 'LikeCnt']
    texts = df.text.to_list()
    sentiments = []
    for text in texts:
        sentiments.append(TextBlob(text).sentiment.polarity)
    df['sentiment'] = sentiments

    file_path = f'{CAR_TYPE}_review_data_youtube_api.csv'
    df.to_csv(file_path)