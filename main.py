import streamlit as st
import pandas as pd

st.set_page_config(page_title="Titanic Data Analysis", layout="centered")

st.title("🚢 Titanic 생존 데이터 분석")
st.write("형제/배우자 수(SibSp), 부모/자녀 수(Parch)와 생존율의 관계를 분석합니다.")

# -----------------------------
# 데이터 불러오기 (캐시 사용)
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("titanic.xlsx")

    # 컬럼명 정리 (공백 제거)
    df.columns = df.columns.str.strip()

    # 컬럼명 통일 (버전 차이 대응)
    rename_dict = {
        "Survival": "Survived",
        "survival": "Survived",
        "Siblings/Spouses Aboard": "SibSp",
        "Parents/Children Aboard": "Parch",
        "sibsp": "SibSp",
        "p
