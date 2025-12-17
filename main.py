import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="가족 수와 생존율 분석", layout="centered")
st.title("🚢 가족 수(SibSp, Parch)와 생존율 분석")
st.write("타이타닉 데이터에서 가족 구성과 생존율의 관계를 분석합니다.")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("fitness data.xlsx")
    return df

df = load_data()

st.subheader("📊 원본 데이터 미리보기")
st.dataframe(df.head())

# -----------------------------
# SibSp 분석
# -----------------------------
st.subheader("1️⃣ 형제/배우자 수(SibSp)와 생존율")

sibsp_survival = (
    df.groupby("SibSp")["Survived"]
    .mean()
    .reset_index()
)

st.dataframe(sibsp_survival)

fig1, ax1 = plt.subplots()
ax1.bar(sibsp_survival["SibSp"], sibsp_survival["Survived"])
ax1.set_xlabel("형제/배우자 수 (SibSp)")
ax1.set_ylabel("생존율")
ax1.set_title("SibSp에 따른 생존율")

st.pyplot(fig1)

st.write(
    """
    ✔ 소규모 가족(1~2명)을 동반한 승객의 생존율이 가장 높은 경향을 보인다.  
    ✔ 가족 수가 너무 많을 경우 이동과 구조가 어려워 생존율이 감소한다.
    """
)

# -----------------------------
# Parch 분석
# -----------------------------
st.subheader("2️⃣ 부모/자녀 수(Parch)와 생존율")

parch_survival = (
    df.groupby("Parch")["Survived"]
    .mean()
    .reset_index()
)

st.dataframe(parch_survival)

fig2, ax2 = plt.subplots()
ax2.bar(parch_survival["Parch"], parch_survival["Survived"])
ax2.set_xlabel("부모/자녀 수 (Parch)")
ax2.set_ylabel("생존율")
ax2.set_title("Parch에 따른 생존율")

st.pyplot(fig2)

st.write(
    """
    ✔ 부모 또는 자녀와 함께 탑승한 경우 생존율이 상대적으로 높다.  
    ✔ 특히 보호가 필요한 어린이 동반 승객의 생존 가능성이 높게 나타난다.
    """
)

# -----------------------------
# 가족 규모 분석
# -----------------------------
st.subheader("3️⃣ 가족 규모(FamilySize)와 생존율")

df["FamilySize"] = df["SibSp"] + df["Parch"] + 1

family_survival = (
    df.groupby("FamilySize")["Survived"]
    .mean()
    .reset_index()
)

st.dataframe(family_survival)

fig3, ax3 = plt.subplots()
ax3.plot(family_survival["FamilySize"], family_survival["Survived"], marker="o")
ax3.set_xlabel("가족 규모")
ax3.set_ylabel("생존율")
ax3.set_title("가족 규모에 따른 생존율 변화")

st.pyplot(fig3)

st.success("✅ 소규모 가족이 생존에 가장 유리하다는 결론을 도출할 수 있습니다.")
