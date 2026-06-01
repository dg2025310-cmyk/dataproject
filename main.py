# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🌡️ 기온 상승 비교")

# CSV 불러오기
df = pd.read_csv("ta_20260601093156.csv")

# 날짜 변환
df["날짜"] = pd.to_datetime(df["날짜"])
df["연도"] = df["날짜"].dt.year

# 연평균 계산
yearly = (
    df.groupby("연도")["평균기온(℃)"]
    .mean()
    .reset_index()
)

# 1980 기준 나누기
before = yearly[yearly["연도"] < 1980]
after = yearly[yearly["연도"] >= 1980]

# 평균 계산
before_avg = before["평균기온(℃)"].mean()
after_avg = after["평균기온(℃)"].mean()

# 결과 표시
st.metric(
    "1980년 이후 상승량",
    f"{after_avg - before_avg:.2f} ℃"
)

# 그래프
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

st.plotly_chart(fig)

# 결론
if after_avg > before_avg:
    st.success("1980년 이후 기온이 상승하는 경향이 보인다.")
else:
    st.warning("뚜렷한 변화가 보이지 않는다.")
