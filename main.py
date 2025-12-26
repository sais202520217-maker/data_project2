import streamlit as st
import pandas as pd

st.set_page_config(page_title="Titanic Data Analysis", layout="centered")

st.title("Titanic 생존 데이터 분석")
st.write("형제/배우자 수(sibsp), 부모/자녀 수(parch)와 생존율의 관계를 분석합니다.")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("titanic.xlsx")

    # 컬럼명 정리: 공백 제거 + 소문자 통일
    df.columns = df.columns.str.strip().str.lower()

    return df


df = load_data()

# -----------------------------
# 컬럼 확인 (디버깅용이지만 남겨도 OK)
# -----------------------------
st.subheader("컬럼 목록 확인")
st.write(df.columns.tolist())

# -----------------------------
# 데이터 미리보기
# -----------------------------
st.subheader("데이터 미리보기")
st.dataframe(df.head())

# -----------------------------
# SibSp 분석
# -----------------------------
st.subheader("형제/배우자 수(sibsp)와 생존율")

if "sibsp" in df.columns and "survived" in df.columns:
    sibsp_survival = (
        df.groupby("sibsp", as_index=False)["survived"]
        .mean()
        .rename(columns={"survived": "survival_rate"})
    )

    st.dataframe(sibsp_survival)
    st.bar_chart(sibsp_survival.set_index("sibsp"))
else:
    st.error("필요한 컬럼(sibsp, survived)이 데이터에 없습니다.")

# -----------------------------
# Parch 분석
# -----------------------------
st.subheader("부모/자녀 수(parch)와 생존율")

if "parch" in df.columns and "survived" in df.columns:
    parch_survival = (
        df.groupby("parch", as_index=False)["survived"]
        .mean()
        .rename(columns={"survived": "survival_rate"})
    )

    st.dataframe(parch_survival)
    st.bar_chart(parch_survival.set_index("parch"))
else:
    st.error("필요한 컬럼(parch, survived)이 데이터에 없습니다.")

# -----------------------------
# 분석 요약
# -----------------------------
st.subheader("분석 요약")
st.markdown(
    "- 혼자 탑승한 승객보다 가족이 1~2명 있는 경우 생존율이 더 높게 나타난다.\n"
    "- 가족 수가 많아질수록 이동이 어려워져 생존율이 낮아지는 경향이 있다.\n"
    "- 가족 구성원 수는 생존에 영향을 주는 주요 요인 중 하나로 해석할 수 있다."
)
