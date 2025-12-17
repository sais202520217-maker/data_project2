import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="가족 수와 생존율 분석", layout="centered")
st.title("🚢 가족 구성과 생존율 분석")

@st.cache_data
def load_data():
    return pd.read_excel("fitness data.xlsx")

df = load_data()

st.subheader("데이터 컬럼 확인")
st.write(df.columns.tolist())

# -------------------------------
# sibsp와 생존율
# -------------------------------
st.subheader("형제/배우자 수(sibsp)와 생존율")

sibsp_survival = df.groupby("sibsp")["survived"].mean()

fig1, ax1 = plt.subplots()
sibsp_survival.plot(kind="bar", ax=ax1)
ax1.set_xlabel("형제/배우자 수 (sibsp)")
ax1.set_ylabel("생존율")
ax1.set_ylim(0, 1)
st.pyplot(fig1)

# -------------------------------
# parch와 생존율
# -------------------------------
st.subheader("부모/자녀 수(parch)와 생존율")

parch_survival = df.groupby("parch")["survived"].mean()

fig2, ax2 = plt.subplots()
parch_survival.plot(kind="bar", ax=ax2)
ax2.set_xlabel("부모/자녀 수 (parch)")
ax2.set_ylabel("생존율")
ax2.set_ylim(0, 1)
st.pyplot(fig2)

# -------------------------------
# 가족 크기
# -------------------------------
st.subheader("가족 규모와 생존율")

df["familysize"] = df["sibsp"] + df["parch"] + 1
family_survival = df.groupby("familysize")["survived"].mean()

fig3, ax3 = plt.subplots()
family_survival.plot(marker="o", ax=ax3)
ax3.set_xlabel("가족 규모")
ax3.set_ylabel("생존율")
ax3.set_ylim(0, 1)
st.pyplot(fig3)

st.info(
    "소규모 가족(2~4명)의 생존율이 가장 높고, "
    "가족 규모가 지나치게 커질수록 생존율이 감소하는 경향을 보입니다."
)
