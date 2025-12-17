import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="Titanic 가족 수와 생존율 분석", layout="wide")

st.title("🚢 타이타닉 가족 수(SibSp, Parch)와 생존율 분석")
st.write("형제/배우자 수, 부모/자녀 수가 생존율에 어떤 영향을 미치는지 분석합니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_excel("titanic.xls")
    return df

df = load_data()

st.subheader("📌 데이터 미리보기")
st.dataframe(df[["Survived", "SibSp", "Parch"]].head())

# ===============================
# SibSp 분석
# ===============================
st.subheader("1️⃣ 형제/배우자 수(SibSp)와 생존율")

sibsp_survival = df.groupby("SibSp")["Survived"].mean()

fig1, ax1 = plt.subplots()
ax1.bar(sibsp_survival.index, sibsp_survival.values)
ax1.set_xlabel("형제/배우자 수 (SibSp)")
ax1.set_ylabel("생존율")
ax1.set_title("SibSp에 따른 생존율")

st.pyplot(fig1)

st.write("""
- 1~2명의 형제/배우자와 함께 탑승한 경우 생존율이 가장 높음  
- 가족 수가 너무 많아질수록 생존율 감소
""")

# ===============================
# Parch 분석
# ===============================
st.subheader("2️⃣ 부모/자녀 수(Parch)와 생존율")

parch_survival = df.groupby("Parch")["Survived"].mean()

fig2, ax2 = plt.subplots()
ax2.bar(parch_survival.index, parch_survival.values)
ax2.set_xlabel("부모/자녀 수 (Parch)")
ax2.set_ylabel("생존율")
ax2.set_title("Parch에 따른 생존율")

st.pyplot(fig2)

st.write("""
- 부모 또는 자녀 1~2명과 동반한 승객의 생존율이 높음  
- 다수 가족 동반 시 생존율 감소
""")

# ===============================
# FamilySize 확장 분석
# ===============================
st.subheader("3️⃣ 가족 수(FamilySize)와 생존율")

df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
family_survival = df.groupby("FamilySize")["Survived"].mean()

fig3, ax3 = plt.subplots()
ax3.plot(family_survival.index, family_survival.values, marker="o")
ax3.set_xlabel("가족 수 (FamilySize)")
ax3.set_ylabel("생존율")
ax3.set_title("가족 수에 따른 생존율")

st.pyplot(fig3)

st.write("""
- 가족 수가 2~4명일 때 생존율이 가장 높음  
- 혼자이거나 대가족일수록 생존율이 낮아지는 경향
""")

st.success("✅ 분석 완료: 가족 구성은 생존율에 중요한 영향을 미침")
