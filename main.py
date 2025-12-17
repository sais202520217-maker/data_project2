import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="가족 구성과 생존율 분석", layout="centered")
st.title("🚢 가족 구성에 따른 생존율 분석 (전처리 포함)")

# -------------------------------
# 데이터 불러오기
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("titanic.xls")

df = load_data()

st.subheader("📄 데이터 컬럼 확인")
st.write(list(df.columns))

# ===============================
# 1️⃣ 결측치 처리
# ===============================
if "age" in df.columns:
    df["age"] = df["age"].fillna(df["age"].median())

if "fare" in df.columns:
    df["fare"] = df["fare"].fillna(df["fare"].median())

# ===============================
# 2️⃣ 이상치 처리 (IQR 방식)
# ===============================
def remove_outliers_iqr(data, column):
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return data[(data[column] >= lower) & (data[column] <= upper)]

if "fare" in df.columns:
    df = remove_outliers_iqr(df, "fare")

# ===============================
# 3️⃣ 정규화 (직접 Min-Max 계산)
# ===============================
def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())

if "age" in df.columns:
    df["age_norm"] = min_max_normalize(df["age"])

if "fare" in df.columns:
    df["fare_norm"] = min_max_normalize(df["fare"])

# ===============================
# 가족 규모 & 생존율 계산
# ===============================
df["familysize"] = df["sibsp"] + df["parch"] + 1
family_survival = df.groupby("familysize", as_index=False)["survived"].mean()

# 최대값 위치 표시
max_survival = family_survival["survived"].max()
family_survival["최대값"] = family_survival["survived"] == max_survival

# ===============================
# Plotly 시각화 (최대값 색상 강조)
# ===============================
fig = px.bar(
    family_survival,
    x="familysize",
    y="survived",
    color="최대값",
    title="가족 규모에 따른 생존율 (최대값 강조)",
    labels={
        "familysize": "가족 구성원 수",
        "survived": "생존율",
        "최대값": "최대 생존율"
    },
    color_discrete_map={
        True: "crimson",
        False: "steelblue"
    },
    range_y=[0, 1]
)

st.plotly_chart(fig, use_container_width=True)

# ===============================
# 분석 요약
# ===============================
st.subheader("📌 분석 요약")

st.info(
    "결측치 처리, 이상치 제거, 정규화 과정을 거친 후 가족 규모에 따른 생존율을 분석한 결과, "
    "특정 가족 규모에서 생존율이 최대값을 보였다. 해당 구간을 색상으로 강조하여 "
    "데이터의 특징을 직관적으로 확인할 수 있었다."
)
