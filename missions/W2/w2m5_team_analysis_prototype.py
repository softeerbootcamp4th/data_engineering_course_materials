import os
import ast
from typing import List

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud


plt.rcParams['font.family'] = 'NanumGothic'
# plt.rcParams['font.family'] = 'AppleGothic'


# 긍정/부정 분할
def split_pos_neg_by_spec_col(
    boundary_col_name: str,
    boundary: float,
    model_name: str,
    df: pd.DataFrame,
) -> List[str]:
    if model_name == "전체":
        pos_df = df[df[boundary_col_name] >= boundary]
        neg_df = df[df[boundary_col_name] < boundary]
    else:
        pos_df = df[(df[boundary_col_name] >= boundary)
                    & (df['연도'] == model_name)]
        neg_df = df[(df[boundary_col_name] < boundary)
                    & (df['연도'] == model_name)]

    pos_texts = pos_df['리뷰'].apply(ast.literal_eval).sum()
    neg_texts = neg_df['리뷰'].apply(ast.literal_eval).sum()
    return pos_texts, neg_texts


# 워드 클라우드 생성
def visualize_wordcloud(
    df: pd.DataFrame,
    year_list: List[int],
) -> plt.Axes:
    if len(year_list) == 0:
        return plt.figure()

    if len(year_list) == 1:
        row, col = 1, 2
    else:
        row, col = 2, len(year_list)
    fig, axes = plt.subplots(row, col, figsize=(15, 10))
    data = []

    for year in year_list:
        bound_value = 5.0 if year != 2023 else 7.0
        pos_texts, neg_texts = split_pos_neg_by_spec_col(
            '평점 평균', bound_value, year, df
        )
        data.append([pos_texts, f"{year} 그랜저 긍정 리뷰(rate >= {bound_value})"])
        data.append([neg_texts, f"{year} 그랜저 부정 리뷰(rate < {bound_value})"])

    for i, (texts, title) in enumerate(data):
        if len(year_list) == 1:
            ax = axes[i]
        else:
            ax = axes[i % row, i//row]
        wc = WordCloud(
            font_path='/usr/share/NanumGothic.ttf',
            # font_path='/Library/Fonts/AppleGothic.ttf',
            background_color='white',
            width=800,
            height=800,
            max_words=100,
            collocations=False
        ).generate(" ".join(texts))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        ax.set_title(title)
        ax.figure.tight_layout()

    fig.tight_layout()
    return fig


def visualize_avg_rate_by_year(df: pd.DataFrame, year_list: List[int]):
    fig, axes = plt.subplots(1, 2, figsize=(20, 12))
    if len(year_list) == 0:
        return fig

    group_df = df[df['연도'].isin(year_list)].groupby('연도')
    avg_rate = group_df['평점 평균'].mean()

    # axes[0]
    axes[0].plot(avg_rate.index, avg_rate.values, marker='o')
    axes[0].set_title('평점 평균 추이')
    axes[0].legend(title="Year")
    axes[0].grid(True)

    # axes[1]
    categories = ['주행성능', '가격', '거주성', '품질', '디자인', '연비']
    num_vars = len(categories)

    pi = 3.14159
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    ax = plt.subplot(122, polar=True)
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    plt.xticks(angles[:-1], categories)

    # Plot each year's data
    for year in year_list:
        values = df[df['연도'] == year][['주행성능', '가격',
                                       '거주성', '품질', '디자인', '연비']].mean().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1,
                linestyle='solid', label=str(year))
        ax.fill(angles, values, alpha=0.1)

    ax.set_title('평점 레이더 차트')
    ax.grid(True)
    ax.legend(loc='upper right')

    return fig


if __name__ == '__main__':
    granduer_df = pd.read_csv('granduer.csv')

    # Title
    st.title("현대자동차 차량 리뷰 분석")
    st.write("<b>(1조): </b> DE 김영일, DE 임태규, DE 최우형",
             unsafe_allow_html=True)
    st.write(
        "네이버 포털 사이트에서 제공하는 오너 평가 리뷰를 기반으로, 차량의 변화(풀체인지, 페이스리프팅)가 있을 때마다 사용자의 실제 리뷰를 분석 및 시각화를 위한 프로토타입입니다."
    )

    # checkbox
    st.sidebar.title("차량 연식 선택")
    ig_first = st.sidebar.checkbox("2017년 그랜저 IG 전기형")
    ig_last = st.sidebar.checkbox("2020년 그랜저 IG 후기형")
    new_granduer = st.sidebar.checkbox("2023년 신형 그랜저")

    st.write("### 샘플 데이터프레임 설명")
    st.dataframe(granduer_df.head())
    st.write("""
    - **차종**: 다양한 차종 (그랜저, 포터, 아이오닉 등)을 분류하기 위한 컬럼입니다.
    - **연도**: 풀체인지/페이스 리프트가 진행되는 해를 기록하기 위한 컬럼입니다.
    - **평점 평균**: 특정 연식의 차량에 대한 사용자들의 차량 만족도 평균 평점을 저장하기 위한 컬럼입니다.
    - **리뷰**: koNLPy를 활용하여 전처리한 리뷰 데이터를 저장하기 위한 컬럼입니다.
    - **공감**: 사용자들이 리뷰에 공감한 수를 저장하기 위한 컬럼입니다.
    - **비공감**: 사용자들이 리뷰에 비공감한 수를 저장하기 위한 컬럼입니다.
    """)

    year_list = []

    if ig_first:
        year_list.append(2017)

    if ig_last:
        year_list.append(2020)

    if new_granduer:
        year_list.append(2023)

    st.write(f"### 연식별 그랜저 리뷰 데이터 분석 결과")
    st.pyplot(visualize_avg_rate_by_year(granduer_df, year_list))

    st.write(f"### 연식별 그랜저 리뷰 데이터 워드 클라우드")
    st.pyplot(visualize_wordcloud(granduer_df, year_list))
