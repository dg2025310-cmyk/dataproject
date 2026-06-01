# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

st.set_page_config(
    page_title="기온 상승 분석",
    layout="wide"
)

st.title("🌍 1980년대 이전·이후 기온 상승 비교")

st.markdown(
    """
이 웹앱은 장기 기온 데이터를 이용해

- 1980년 이전
- 1980년 이후

기온 변화 추세가 얼마나 다른지 분석한다.

가설:

> "1980년 이후 기온 상승 속도가 더 빨라졌다."
"""
)

# -----------------------------
# 데이터 불러오기
# -----------------------------

uploaded_file = st.file_uploader(
    "CSV 파일 업로드",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("ta_20260601093156.csv")

# -----------------------------
# 데이터 전처리
# -----------------------------

df["날짜"] = df["날짜"].astype(str).str.strip()
df["날짜"] = pd.to_datetime(df["날짜"])

df["연도"] = df["날짜"].dt.year

yearly = (
    df.groupby("연도")["평균기온(℃)"]
    .mean()
    .reset_index()
)

# -----------------------------
# 기준 연도 선택
# -----------------------------

split_year = st.slider(
    "비교 기준 연도 선택",
    min_value=int(yearly["연도"].min()),
    max_value=int(yearly["연도"].max()),
    value=1980
)

before = yearly[yearly["연도"] < split_year]
after = yearly[yearly["연도"] >= split_year]

# -----------------------------
# 선형 회귀 분석
# -----------------------------

before_result = linregress(
    before["연도"],
    before["평균기온(℃)"]
)

after_result = linregress(
    after["연도"],
    after["평균기온(℃)"]
)

before_slope = before_result.slope
after_slope = after_result.slope

# -----------------------------
# 결과 카드
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric(
        f"{split_year}년 이전 상승 속도",
        f"{before_slope:.4f} ℃/년"
    )

with col2:
    st.metric(
        f"{split_year}년 이후 상승 속도",
        f"{after_slope:.4f} ℃/년"
    )

# -----------------------------
# 그래프
# -----------------------------

fig, ax = plt.subplots(figsize=(12, 6))

# 실제 데이터
ax.plot(
    yearly["연도"],
    yearly["평균기온(℃)"],
    linewidth=2,
    label="연평균 기온"
)

# 이전 추세선
ax.plot(
    before["연도"],
    before_result.intercept + before_slope * before["연도"],
    linestyle="--",
    linewidth=3,
    label=f"{split_year} 이전 추세선"
)

# 이후 추세선
ax.plot(
    after["연도"],
    after_result.intercept + after_slope * after["연도"],
    linestyle="--",
    linewidth=3,
    label=f"{split_year} 이후 추세선"
)

# 기준선
ax.axvline(split_year, linestyle=":", linewidth=2)

ax.set_title("연평균 기온 변화")
ax.set_xlabel("연도")
ax.set_ylabel("평균기온 (℃)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# -----------------------------
# 가설 판정
# -----------------------------

st.subheader("📌 가설 분석 결과")

if after_slope > before_slope:
    st.success(
        "1980년 이후 기온 상승 속도가 더 빠르다는 가설을 지지한다."
    )
else:
    st.warning(
        "1980년 이후 상승 속도가 특별히 더 빠르다고 보기 어렵다."
    )

# -----------------------------
# 상세 통계
# -----------------------------

st.subheader("📊 상세 통계")

stats_df = pd.DataFrame({
    "구간": [
        f"~ {split_year-1}",
        f"{split_year} ~"
    ],
    "기울기(℃/년)": [
        before_slope,
        after_slope
    ],
    "상관계수": [
        before_result.rvalue,
        after_result.rvalue
    ],
    "p-value": [
        before_result.pvalue,
        after_result.pvalue
    ]
})

st.dataframe(stats_df, use_container_width=True)

# -----------------------------
# 데이터 보기
# -----------------------------

with st.expander("원본 연도별 데이터 보기"):
    st.dataframe(yearly, use_container_width=True)
