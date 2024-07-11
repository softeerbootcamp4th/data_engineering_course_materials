import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

FONT_PATH = 'SeoulNamsanB.ttf'
ZIGBANG_API_URL = 'https://apis.zigbang.com/v2/local/price?geohash=&local_level=3&period=1&transaction_type_eq=s'

response = requests.get(ZIGBANG_API_URL)
json = response.json()['datas']

columns = [ "bjdCode", "local1", "local2", "local3", "변동률",]
df = pd.json_normalize(json)[columns]
non_null_df = df.dropna(subset='변동률').copy()


st.write("# 집값 변동률")
city = st.text_input("지역")
if city:
    filtered_df = non_null_df[
        non_null_df.apply(lambda row: city in row['local1'] or city in row['local2'] or city in row['local3'], axis=1)
    ]

    filtered_df.loc[:, 'local2_3'] = filtered_df['local2'] + ' ' + filtered_df['local3']
    pos_change_rate_area_df = filtered_df[filtered_df['변동률'] > 0]
    neg_change_rate_area_df = filtered_df[filtered_df['변동률'] < 0]
    pos_change_rate_area_dict = pos_change_rate_area_df.set_index('local2_3')['변동률'].to_dict()
    neg_change_rate_area_dict = neg_change_rate_area_df.set_index('local2_3')['변동률'].to_dict()

    max_cities = 100
    pos_word_cloud = WordCloud(
        max_words=max_cities,
        width=600,
        height=600,
        min_font_size=7,
        font_path=FONT_PATH).generate_from_frequencies(pos_change_rate_area_dict)

    neg_word_cloud = WordCloud(
        max_words=max_cities,
        width=600,
        height=600,
        min_font_size=7,
        font_path=FONT_PATH).generate_from_frequencies(neg_change_rate_area_dict)

    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    axes[0].imshow(pos_word_cloud, interpolation='bilinear')
    axes[0].set_title("Positive Change Rate Word Cloud", fontsize=24)
    axes[0].axis("off")

    axes[1].imshow(neg_word_cloud, interpolation='bilinear')
    axes[1].set_title("Negative Change Rate Word Cloud", fontsize=24)
    axes[1].axis("off")

    st.pyplot(fig)