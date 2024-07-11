import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Define the URL of the FastAPI server
API_URL = "http://127.0.0.1:8000/word_freq/"

# List of options for the dropdown menu
options = ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시',
           '세종특별자치시', '경기도', '충청북도', '충청남도', '전라남도', '경상북도', '경상남도',
           '제주특별자치도', '강원특별자치도', '전북특별자치도']

# Streamlit app
st.title("동네별 매매가 변동률 확인")

# Dropdown menu for 'local1'
local1 = st.selectbox("행정구역 선택", options)

# Generate word clouds button
if st.button("Word Cloud 생성"):
    # Send POST request to FastAPI server
    response = requests.post(API_URL, json={"local1": local1})
    
    if response.status_code == 200:
        data = response.json()
        
        word_freq_positive = data.get("word_freq_positive", {})
        word_freq_negative = data.get("word_freq_negative", {})
        
        # Generate word clouds
        wordcloud_positive = WordCloud(width=800, height=400, background_color='white', font_path='NanumGothic.ttf').generate_from_frequencies(word_freq_positive)
        wordcloud_negative = WordCloud(width=800, height=400, background_color='white', font_path='NanumGothic.ttf').generate_from_frequencies(word_freq_negative)
        
        # Display word clouds
        st.header("높은 매매가 상승률")
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud_positive, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)
        
        st.header("높은 매매가 하락률")
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud_negative, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)
    else:
        st.error("Error fetching data from FastAPI server")

# Run the app
# In terminal, run: streamlit run app.py
