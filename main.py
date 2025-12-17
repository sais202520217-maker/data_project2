import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정 (Streamlit/리눅스 환경 대응)
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="가족 구성과 생존율 분석", layout="centered")
st.title("🚢 가족 구성에 따른 생존율 분석")

# 데이터 불러오기
@st.cache_data
def load_data():
    return pd.read_excel("titanic.xls")

df = load_data()

st.subheader("📄 데이터 컬럼 확인")
st.write(df.columns)

# -------------------------------
# 형제/배우자 수와 생존율
# -------------------------------
st.subheader("👨‍👩‍👧 형제/배우자 수와 생존율")

sibsp_survival = df.groupby("sibsp")["survived"].mean()

fig1, ax1 = plt.subplots()
sibsp_survival.plot(kind="bar", ax=ax1)

ax1.set_title("형제/배우자 수에 따른 생존율")
ax1.set_xlabel("형제 / 배우자 수")
ax1.set_ylabel("생존율")
ax1.set_ylim(0, 1)

st.pyplot(fig1)

st.caption("※ 1~2명의 형제 또는 배우자와 함께 탑승한 경우 생존율이 높게 나타남")

# -------------------------------
# 부모/자녀 수와 생존율
# -------------------------------
st.subheader("👪 부모/자녀 수와 생존율")

parch_survival = df.groupby("parch")["survived"].mean()

fig2, ax2 = plt.subplots()
parch_survival.plot(kind="bar", ax=ax2)

ax2.set_title("부모/자녀 수에 따른 생존율")
ax2.set_xlabel("부모 / 자녀 수")
ax2.set_ylabel("생존율")
ax2.set_ylim(0, 1)

st.pyplot(fig2)

st.caption("※ 부모 또는 자녀와 동반 탑승한 경우 상대적으로 생존율이 높음")

# -------------------------------
# 가족 규모와 생존율
# -------------------------------
st.subheader("🏠 가족 규모와 생존율")

df["familysize"] = df["sibsp"] + df["parch"] + 1
family_survival = df.groupby("familysize")["survived"].mean()

fig3, ax3 = plt.subplots()
family_survival.plot(marker="o", ax=ax3)

ax3.set_title("가족 규모에 따른 생존율 변화")
ax3.set_xlabel("가족 구성원 수")
ax3.set_ylabel("생존율")
ax3.set_ylim(0, 1)

st.pyplot(fig3)

# -------------------------------
# 분석 요약
# -------------------------------
st.subheader("📌 분석 요약 (세특 활용 가능)")

st.info(
    "분석 결과, 혼자 탑승한 승객보다 2~4명의 소규모 가족과 함께 탑승한 경우 생존율이 가장 높게 나타났다. "
    "반면 가족 규모가 지나치게 커질수록 생존율은 감소하는 경향을 보였으며, "
    "이는 위기 상황에서 소규모 가족 단위의 이동과 협력이 상대적으로 유리했기 때문으로 해석할 수 있다."
)
