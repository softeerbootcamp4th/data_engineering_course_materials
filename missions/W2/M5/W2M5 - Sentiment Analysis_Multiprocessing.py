# 필요한 라이브러리 임포트
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud
from multiprocessing import Process
from multiprocessing import Manager
from collections import Counter

# 데이터셋 불러오기 (csv 파일 경로를 지정)
df = pd.read_csv('training.1600000.processed.noemoticon.csv', encoding='latin1')

# 데이터프레임 컬럼 명 설정
df.columns = ['target', 'id', 'timestamp', 'flag', 'user', 'text']

# 긍정 및 부정 트윗 필터링
positive_tweets = df[df['target'] == 4]['text']
negative_tweets = df[df['target'] == 0]['text']

# 멀티 프로세스로 수행할 전처리 함수
def preprocess(texts : list[str], return_list):
    tokens = []
    
    for text in texts:
        text = text.lower()
        text = re.sub(r"[^a-z']", ' ', text)
        tokens.extend(text.split())
    
    return_list.extend(tokens)
    
    
def preprocess_(texts : list[str]):
    tokens = []
    
    for text in texts:
        text = text.lower()
        text = re.sub(r"[^a-z']", ' ', text)
        tokens.extend(text.split())
    
    return len(tokens)


# 단어 샘플링 함수
def sample_words(tokens, max_words=200):
    # all_words = [word for tokens_list in tokens for word in tokens_list]
    all_words = [word for word in tokens]
    word_counts = Counter(all_words)
    most_common_words = word_counts.most_common(max_words)
    return dict(most_common_words)


# Word Cloud 생성 함수
def create_wordcloud(word_freq, title):
    wordcloud = WordCloud(width=800, height=400, max_words=200, background_color='white').generate_from_frequencies(word_freq)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title, fontsize=20)
    plt.axis('off')
    plt.show()


# main
if __name__ == "__main__":
    manager = Manager()
    return_pos_list = manager.list()
    return_neg_list = manager.list()
    processes = []
    number_of_processes = 4

    chunk_size = len(positive_tweets) // number_of_processes
    chunks = [positive_tweets[i * chunk_size : (i + 1) * chunk_size] for i in range(number_of_processes - 1)]
    chunks.append(positive_tweets[(number_of_processes - 1) * chunk_size:])  # 마지막 청크 추가
    
    neg_chunk_size = len(negative_tweets) // number_of_processes
    neg_chunks = [negative_tweets[i * neg_chunk_size : (i + 1) * neg_chunk_size] for i in range(number_of_processes - 1)]
    neg_chunks.append(negative_tweets[(number_of_processes - 1) * neg_chunk_size:])  # 마지막 청크 추가

    # creating processes
    for i in range(number_of_processes):
        chunk = chunks[i]
        p = Process(target=preprocess, args=(chunk, return_pos_list))    
        processes.append(p)
        print(f"pos_process {i}")
        p.start()

    for i in range(number_of_processes):
        neg_chunk = neg_chunks[i]
        p = Process(target=preprocess, args=(neg_chunk, return_neg_list))    
        processes.append(p)
        print(f"neg_process {i}")
        p.start()
        
    # completing process
    for p in processes:
        p.join()
    
    # 긍정 및 부정 트윗 샘플링    
    positive_word_freq = sample_words(return_pos_list)
    negative_word_freq = sample_words(return_neg_list)

    # 긍정 및 부정 감정에 대한 Word Cloud 생성
    create_wordcloud(positive_word_freq, 'Positive Sentiment Word Cloud')
    create_wordcloud(negative_word_freq, 'Negative Sentiment Word Cloud')