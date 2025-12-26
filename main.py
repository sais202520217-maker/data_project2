import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# 페이지 설정
# -------------------------------
st.set_page_config(
    page_title="가족 구성과 생존율 분석",
    layout="centered"
)

st.title("🚢 가족 구성에 따른 생존율 분석")

# -------------------------------
# 데이터 불러오기
# -------------------------------
@st.cache_data
def load_data():
    # 파일명이 titanic.xlsx 인 경우
    return pd.read_excel("titanic.xls")

df = load_data()

st.subheader("📄 데이터 컬럼 확인")
st.write(list(df.columns))

# -------------------------------
# 형제/배우자 수와 생존율
# -------------------------------
st.subheader("👨‍👩‍👧 형제/배우자 수와 생존율")

sibsp_survival = (
    df.groupby("SibSp", as_index=False)["Survived"].mean()
)

fig1 = px.bar(
    sibsp_survival,
    x="SibSp",
    y="Survived",
    title="형제/배우자 수에 따른 생존율",
    labels={
        "SibSp": "형제 / 배우자 수",
        "Survived": "생존율"
    },
    range_y=[0, 1]
)

st.plotly_chart(fig1, use_container_width=True)

st.caption("※ 1~2명의 형제 또는 배우자와 함께 탑승한 경우 생존율이 높게 나타남")

# -------------------------------
# 부모/자녀 수와 생존율
# -------------------------------
st.subheader("👪 부모/자녀 수와 생존율")

parch_survival = (
    df.groupby("Parch", as_index=False)["Survived"].mean()
)

fig2 = px.bar(
    parch_survival,
    x="Parch",
    y="Survived",
    title="부모/자녀 수에 따른 생존율",
    labels={
        "Parch": "부모 / 자녀 수",
        "Survived": "생존율"
    },
    range_y=[0, 1]
)

st.plotly_chart(fig2, use_container_width=True)

st.caption("※ 부모 또는 자녀와 동반 탑승한 승객의 생존율이 상대적으로 높음")

# -------------------------------
# 가족 규모와 생존율
# -------------------------------
st.subheader("🏠 가족 규모와 생존율")

df["FamilySize"] = df["SibSp"] + df["Parch"] + 1

family_survival = (
    df.groupby("FamilySize", as_index=False)["Survived"].mean()
)

fig3 = px.line(
    family_survival,
    x="FamilySize",
    y="Survived",
    markers=True,
    title="가족 규모에 따른 생존율 변화",
    labels={
        "FamilySize": "가족 구성원 수",
        "Survived": "생존율"
    },
    range_y=[0, 1]
)

st.plotly_chart(fig3, use_container_width=True)

# -------------------------------
# 분석 요약
# -------------------------------
st.subheader("📌 분석 요약 (세특 활용 가능)")

st.info(
    "분석 결과, 혼자 탑승한 경우보다 2~4명의 소규모 가족과 함께 탑승한 경우 "
    "생존율이 가장 높게 나타났다. 반면 가족 규모가 커질수록 생존율은 감소하는 "
    "경향을 보였으며, 이는 위기 상황에서 소규모 가족 단위의 이동과 협력이 "
    "상대적으로 유리했기 때문으로 해석할 수 있다."
)
