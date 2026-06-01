# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------
# 기본 설정
# -------------------

st.set_page_config(
    page_title="기온 변화 분석",
    page_icon="🌍",
    layout="centered"
)

# -------------------
# 제목
# -------------------

st.markdown(
    """
    <h1 style='text-align:center;'>
    🌍 기온 변화 분석
    </h1>
    <p style='text-align:center; color:gray;'>
    1980년 전후 평균기온 비교
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------
# 데이터 불러오기
# -------------------

df = pd.read_csv("ta_20260601093156.csv")

df["날짜"] = pd.to_datetime(df["날짜"])
df["연도"] = df["날짜"].dt.year

yearly = (
    df.groupby("연도")["평균기온(℃)"]
    .mean()
    .reset_index()
)

# -------------------
# 평균 계산
# -------------------

before = yearly[yearly["연도"] < 1980]
after = yearly[yearly["연도"] >= 1980]

before_avg = before["평균기온(℃)"].mean()
after_avg = after["평균기온(℃)"].mean()

diff = after_avg - before_avg

# -------------------
# 요약 카드
# -------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "1980년 이전",
        f"{before_avg:.2f} ℃"
    )

with col2:
    st.metric(
        "1980년 이후",
        f"{after_avg:.2f} ℃"
    )

with col3:
    st.metric(
        "상승량",
        f"{diff:.2f} ℃"
    )

st.divider()

# -------------------
# 그래프
# -------------------

fig = px.line(
    yearly,
    x="연도",
    y="평균기온(℃)",
    markers=True
)

fig.add_vline(
    x=1980,
    line_dash="dash"
)

# 그래프 크기 조절
fig.update_layout(
    height=420,
    margin=dict(l=20, r=20, t=30, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------
# 결론
# -------------------

st.subheader("📌 분석 결과")

if diff > 0:
    st.success(
        f"1980년 이후 평균기온이 "
        f"{diff:.2f}℃ 상승하였다."
    )
else:
    st.warning(
        "뚜렷한 상승 경향이 보이지 않는다."
    )

# -------------------
# 데이터 표
# -------------------

with st.expander("연도별 데이터 보기"):
    st.dataframe(
        yearly,
        use_container_width=True
    )
