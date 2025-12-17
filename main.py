import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="가족 규모와 생존 분석", layout="centered")
st.title("🚢 가족 규모에 따른 생존 분석 (산점도)")

# --------------------
# 데이터 로드
# --------------------
@st.cache_data
def load_data():
    return pd.read_excel("titanic.xls")

df = load_data()

# --------------------
# 필요한 컬럼만 사용
# --------------------
needed_cols = ["sibsp", "parch", "survived"]
df = df[needed_cols]

# 결측치 제거
df = df.dropna()

# --------------------
# 가족 규모 생성
# --------------------
df["familysize"] = df["sibsp"] + df["parch"] + 1

# --------------------
# 통계 계산
# --------------------
family_stats = (
    df.groupby("familysize")
      .agg(
          생존률=("survived", "mean"),
          생존자수=("survived", "sum"),
          전체인원=("survived", "count")
      )
      .reset_index()
)

max_rate = family_stats["생존률"].max()
family_stats["최대생존률"] = family_stats["생존률"] == max_rate

# --------------------
# 산점도 시각화
# --------------------
fig = px.scatter(
    family_stats,
    x="familysize",
    y="생존률",
    size="전체인원",
    color="최대생존률",
    hover_data=["생존자수", "전체인원"],
    labels={
        "familysize": "가족 구성원 수",
        "생존률": "생존률",
        "전체인원": "해당 가족 규모 인원 수"
    },
    title="가족 규모에 따른 생존률 산점도",
    color_discrete_map={
        True: "crimson",
        False: "steelblue"
    }
)

st.plotly_chart(fig, use_container_width=True)

# --------------------
# 표 출력
# --------------------
st.subheader("📊 가족 규모별 생존 통계")
st.dataframe(family_stats, use_container_width=True)
