from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import pandas as pd
import os
import yaml

# youtube의 video id 가 담겨있는 json load
with open('/Users/admin/Desktop/Data_Engineering/W2/youtube/W2M5_car_extract_setting.json', 'r') as f:
    settings = json.load(f)

# File path, api 가 담겨있는 yaml file load
with open('/Users/admin/Desktop/Data_Engineering/W2/youtube/W2M5_setting.yaml', 'r') as file:
    config = yaml.safe_load(file)

# api_key 가져오기
api_key = config['key']['api_key']

def get_comments(video_id):
    comments = []
    try:
        # Youtube Comment를 가져오는 YouTube Data API v3 객체 생성
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.commentThreads().list( # CommentThread resource에 대한 list method 호출
            part='snippet,replies', # 댓글과 대댓글 전부 가져옴
            videoId=video_id, # 가져올 video id 할당
            maxResults=100 # 한 번의 요청으로 반환받을 최대 댓글 스레드 수. 최대로 설정
        )
        response = request.execute()

        while request:
            for item in response['items']:
                top_level_comment = item['snippet']['topLevelComment']['snippet'] # Top level Comment 추출
                user_name = top_level_comment['authorDisplayName'] # user id 가져오기
                comment_text = top_level_comment['textOriginal']  # 원어 그대로 가져오기 위해 textDisplay 대신 textOriginal 사용
                like_count = top_level_comment['likeCount'] # Top level Comment의 좋아요 수 추출
                comments.append({'User Name': user_name, 'Comment': comment_text, 'Likes': like_count})

                # Top level Comment에 대댓글이 있는지 확인
                if 'replies' in item:
                    for reply in item['replies']['comments']: # 대댓글이 있다면 위와 같은 방법으로 Data Extraction
                        reply_user_name = reply['snippet']['authorDisplayName']
                        reply_comment_text = reply['snippet']['textOriginal']
                        reply_like_count = reply['snippet']['likeCount']
                        comments.append({'User Name': reply_user_name, 'Comment': reply_comment_text, 'Likes': reply_like_count})

            if 'nextPageToken' in response: # maxResults의 최대값이 100이기 때문에 남은 Comment가 있다면 다시 Extraction
                request = youtube.commentThreads().list(
                    part='snippet,replies',
                    videoId=video_id,
                    pageToken=response['nextPageToken'],
                    maxResults=100
                )
                response = request.execute()
            else:
                break
    # Error 처리
    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return comments

# "Youtube_Comment" 폴더 생성
output_folder = "Youtube_Comment"
os.makedirs(output_folder, exist_ok=True)

# 각 차량별로 댓글을 가져와서 CSV 파일로 저장
for car_model, video_ids in settings.items():
    all_comments = []
    for video_id in video_ids:
        comments = get_comments(video_id)
        all_comments.extend(comments)
    
    # Comment를 DataFrame으로 변환
    df = pd.DataFrame(all_comments)
    
    # DataFrame을 {car_model}_youtube_comments.csv로 저장
    file_name = os.path.join(output_folder, f'{car_model}_youtube_comments.csv')
    df.to_csv(file_name, index=False, encoding='utf-8-sig')  # UTF-8 Incoding with BOM for Excel 호환성
    
    print(f"{file_name} Extraction Success.")
