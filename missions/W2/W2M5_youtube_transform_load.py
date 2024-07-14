import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
import nltk
from collections import Counter
import yaml

# YAML 파일에서 설정 읽기
with open('/Users/admin/Desktop/Data_Engineering/W2/youtube/W2M5_setting.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Extraction으로 부터 받은 folder path 설정
input_folder = config['paths']['input_folder']
output_folder = config['paths']['output_folder']
wordcloud_folder = config['paths']['wordcloud_folder']

# Comment Semtiment를 저장할 Folder 생성
os.makedirs(output_folder, exist_ok=True)
os.makedirs(wordcloud_folder, exist_ok=True)

# nltk를 통해 의미없는 word list 생성
stop_words = set(stopwords.words('english'))

# 의미없는 word를 제거한 text 반환
def remove_stopwords(text):
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

# Sentiment 분석
def analyze_sentiment(comment):
    blob = TextBlob(comment)
    return blob.sentiment.polarity

# Word Frequency 함수
def get_word_frequencies(text):
    words = word_tokenize(text)
    return Counter(words)

# CSV 파일에 대해 Sentiment Analysis 수행
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        # csv file을 DataFrame으로 가져옴
        df = pd.read_csv(os.path.join(input_folder, file_name))
        
        # NaN 값을 빈 문자열로 대체
        df['Comment'] = df['Comment'].fillna('')
        # 의미없는 word 제거
        df['Filtered_Comment'] = df['Comment'].apply(remove_stopwords)
        # 각 Comment에 대해 Sentiment Analysis
        df['Sentiment'] = df['Filtered_Comment'].apply(analyze_sentiment)

        # Positive, Negative Comment Filtering (-1 <= Negative < -0.3, -0.3 <= Neutral< 0.3, 0.3 <= Positive < 1) 로 설정
        positive_df = df[df['Sentiment'] > 0.3]
        negative_df = df[df['Sentiment'] < -0.3]

        # Comment Join
        positive_texts = ' '.join(positive_df['Comment'])
        negative_texts = ' '.join(negative_df['Comment'])

        # Word Frequency 계산
        positive_freq = get_word_frequencies(positive_texts)
        negative_freq = get_word_frequencies(negative_texts)

        # Common word 찾기
        common_words = set(positive_freq.keys()) & set(negative_freq.keys())
        common_words = {word for word in common_words if positive_freq[word] > 1 and negative_freq[word] > 1}

        # Common word를 제거한 text Join
        filtered_positive_texts = ' '.join([word for word in word_tokenize(positive_texts) if word not in common_words])
        filtered_negative_texts = ' '.join([word for word in word_tokenize(negative_texts) if word not in common_words])

        # Vehicle 이름만 추출하기 위해 csv file에서 '_youtube_comments' 제거
        car_name = os.path.splitext(file_name)[0].replace('_youtube_comments', '')

        # Plot
        plt.figure(figsize=(16, 8))
        # Positive Word Cloud
        if filtered_positive_texts:
            wordcloud_positive = WordCloud(width=800, height=400, background_color='white', colormap='magma', max_words=200).generate(filtered_positive_texts)
            plt.subplot(1, 2, 1)
            plt.imshow(wordcloud_positive, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'{car_name} Positive Word Cloud', fontsize=20)
        # Negative Word Cloud
        if filtered_negative_texts:
            wordcloud_negative = WordCloud(width=800, height=400, background_color='white', colormap='magma', max_words=200).generate(filtered_negative_texts)
            plt.subplot(1, 2, 2)
            plt.imshow(wordcloud_negative, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'{car_name} Negative Word Cloud', fontsize=20)
        
        # Sentiment Analysis를 포함한 csv file Save
        output_file_name = os.path.join(output_folder, f'{car_name}_Sentiment.csv')
        df.to_csv(output_file_name, index=False, encoding='utf-8')

        # Word Cloud Image Save
        wordcloud_file_name = os.path.join(wordcloud_folder, f'{car_name}_wordcloud.png')
        plt.savefig(wordcloud_file_name)
        plt.close()
 
        print(f"{output_file_name} and {wordcloud_file_name} saved successfully.")

print("Youtube comments with Sentiment Analysis completed successfully.")
