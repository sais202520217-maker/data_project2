import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Titanic Data Analysis", layout="centered")

st.title("Titanic 생존 데이터 분석")
st.write("형제/배우자 수(sibsp), 부모/자녀 수(parch)와 생존율 및 인원 수를 함께 분석합니다.")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("titanic.xlsx")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

# -----------------------------
# 컬럼 확인
# -----------------------------
st.subheader("컬럼 목록")
st.write(df.columns.tolist())

# -----------------------------
# SibSp 분석
# -----------------------------
st.subheader("형제/배우자 수(sibsp)와 생존율")

if "sibsp" in df.columns and "survived" in df.columns:
    sibsp_stats = (
        df.groupby("sibsp")
        .agg(
            survival_rate=("survived", "mean"),
            count=("survived", "count")
        )
        .reset_index()
    )

    st.dataframe(sibsp_stats)

    sibsp_chart = (
        alt.Chart(sibsp_stats)
        .mark_bar()
        .encode(
            x=alt.X("sibsp:O", title="형제/배우자 수"),
            y=alt.Y("survival_rate:Q", title="생존율"),
            tooltip=[
                alt.Tooltip("sibsp:O", title="형제/배우자 수"),
                alt.Tooltip("survival_rate:Q", title="생존율", format=".2f"),
                alt.Tooltip("count:Q", title="인원 수(명)")
            ]
        )
    )

    st.altair_chart(sibsp_chart, use_container_width=True)

else:
    st.error("필요한 컬럼(sibsp, survived)이 없습니다.")

# -----------------------------
# Parch 분석
# -----------------------------
st.subheader("부모/자녀 수(parch)와 생존율")

if "parch" in df.columns and "survived" in df.columns:
    parch_stats = (
        df.groupby("parch")
        .agg(
            survival_rate=("survived", "mean"),
            count=("survived", "count")
        )
        .reset_index()
    )

    st.dataframe(parch_stats)

    parch_chart = (
        alt.Chart(parch_stats)
        .mark_bar()
        .encode(
            x=alt.X("parch:O", title="부모/자녀 수"),
            y=alt.Y("survival_rate:Q", title="생존율"),
            tooltip=[
                alt.Tooltip("parch:O", title="부모/자녀 수"),
                alt.Tooltip("survival_rate:Q", title="생존율", format=".2f"),
                alt.Tooltip("count:Q", title="인원 수(명)")
            ]
        )
    )

    st.altair_chart(parch_chart, use_container_width=True)

else:
    st.error("필요한 컬럼(parch, survived)이 없습니다.")

# -----------------------------
# 분석 요약
# -----------------------------
st.subheader("분석 요약")
st.markdown(
    "- 가족 구성원이 1~2명인 경우 생존율이 상대적으로 높게 나타난다.\n"
    "- 가족 수가 많아질수록 생존율이 감소하는 경향을 보인다.\n"
    "- 막대그래프의 툴팁을 통해 각 범주별 생존율과 실제 인원 수를 함께 확인할 수 있다."
)
