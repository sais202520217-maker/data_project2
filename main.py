import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# 기본 설정
# -------------------------------
st.set_page_config(page_title="가족 수와 생존율 분석", layout="centered")
st.title("🚢 가족 구성과 생존율 분석")
st.write("형제/배우자 수(SibSp), 부모/자녀 수(Parch)가 생존율에 미치는 영향 분석")

# -------------------------------
# 데이터 불러오기
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("titanic.xls")

df = load_data()

st.subheader("📄 데이터 미리보기")
st.dataframe(df.head())

# -------------------------------
# SibSp 생존율 분석
# -------------------------------
st.subheader("👨‍👩‍👧 형제/배우자 수(SibSp)와 생존율")

sibsp_survival = df.groupby("SibSp")["Survived"].mean()

fig1, ax1 = plt.subplots()
sibsp_survival.plot(kind="bar", ax=ax1)
ax1.set_xlabel("형제/배우자 수 (SibSp)")
ax1.set_ylabel("생존율")
ax1.set_ylim(0, 1)
st.pyplot(fig1)

st.write("👉 **1~2명의 형제/배우자와 함께 탑승한 경우 생존율이 가장 높은 경향**")

# -------------------------------
# Parch 생존율 분석
# -------------------------------
s
