import streamlit as st
import pandas as pd

st.set_page_config(page_title="Titanic Data Analysis", layout="centered")

st.title("Titanic 생존 데이터 분석")
st.write("형제/배우자 수(SibSp), 부모/자녀 수(Parch)와 생존율의 관계를 분석합니다.")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("titanic.xlsx")

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    # 컬럼명 통일
    df = df.rename(columns={
        "Survival": "Survived",
        "survival": "Survived",
        "Siblings/Spouses Aboard": "SibSp",
        "Parents/Children Aboard": "Parch",
        "sibsp": "SibSp",
        "parch": "Parch"
    })

    return df


df = load_data()

# -----------------------------
# 데이터 확인
# -----------------------------
st.subheader("데이터 미리보기")
st.dataframe(df.head())

st.subheader("컬럼 목록")
st.write(list(df.columns))

# -----------------------------
# SibSp 분석
# -----------------------------
st.subheader("형제/배우자 수(SibSp)와 생존율")

if "SibSp" in df.columns and "Survived" in df.columns:
    sibsp_survival = (
        df.groupby("SibSp", as_index=False)["survived"]
        .mean()
        .rename(columns={"Survived": "Survival Rate"})
    )

    st.dataframe(sibsp_survival)
    st.bar_chart(sibsp_survival.set_index("sibsp"))
else:
    st.error("SibSp 또는 Survived 컬럼이 없습니다.")

# -----------------------------
# Parch 분석
# -----------------------------
st.subheader("부모/자녀 수(Parch)와 생존율")

if "Parch" in df.columns and "Survived" in df.columns:
    parch_survival = (
        df.groupby("Parch", as_index=False)["survived"]
        .mean()
        .rename(columns={"Survived": "Survival Rate"})
    )

    st.dataframe(parch_survival)
    st.bar_chart(parch_survival.set_index("parch"))
else:
    st.error("Parch 또는 Survived 컬럼이 없습니다.")

# -----------------------------
# 결론
# -----------------------------
st.subheader("분석 요약")
st.markdown(
    "- 혼자 탑승한 승객보다 가족이 1~2명 있는 경우 생존율이 높다.\n"
    "- 가족 수가 너무 많아질 경우 생존율이 감소하는 경향이 있다.\n"
    "- 이는 위기 상황에서 이동성과 구조 우선순위의 영향으로 해석할 수 있다."
)
