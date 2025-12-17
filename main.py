import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="가족 구성과 생존율 분석", layout="centered")

st.title("🚢 타이타닉 생존율 분석")
st.subheader("형제/배우자 수(SibSp), 부모/자녀 수(Parch)와 생존율 비교")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_excel("fitness data.xlsx")
    return df

df = load_data()

st.write("### 📄 데이터 미리보기")
st.dataframe(df.head())

# ===============================
# SibSp 생존율 분석
# ===============================
st.write("## 👨‍👩‍👧 형제/배우자 수(SibSp)와 생존율")

sibsp_survival = df.groupby("SibSp")["Survived"].mean()

fig1, ax1 = plt.subplots()
sibsp_survival._
