import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="가족 구성과 생존 분석", layout="centered")
st.title("🚢 가족 구성에 따른 생존 분석 (생존률 + 생존자 수)")

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
#if "age" in df.columns:
#    df["age"] = df["age"].fillna(df["age"].median())
#
#if "fare" in df.columns:
#    df["fare"] = df["fare"].fillna(df["fare"].median())

# ===============================
# 2️⃣ 이상치 처리 (IQR)
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
# 3️⃣ 정규화 (Min-Max 직접 구현)
# ===============================
def min_max_normalize(series):
    return (series - series.min()) / (series.max() - series.min())

if "age" in df.columns:
    df["age_norm"] = min_max_normalize(df["age"])

if "fare" in df.columns:
    df["fare_norm"] = min_max_normalize(df["fare"])

# ===============================
# 가족 규모 생성
# ===============================
df["familysize"] = df["sibsp"] + df["parch"] + 1

# ===============================
# 생존률 + 생존자 수 계산
# ===============================
family_stats = (
    df.groupby("familysize")
      .agg(
          생존률=("survived", "mean"),
          생존자수=("survived", "sum"),
          전체인원=("survived", "count")
      )
      .reset_index()
)

# 최대 생존률 표시용 컬럼
max_rate = family_stats["생존률"].max()
family_stats["최대생존률"] = family_stats["생존률"] == max_rate

# ===============================
# Plotly 그래프 (생존률 + 생존자 수)
# ===============================
# fig = px.bar(
#     family_stats,
#     x="familysize",
#     y="생존률",
#     color="최대생존률",
#     text="생존자수",
#     title="가족 규모에 따른 생존률 및 생존자 수",
#     labels={
#         "familysize": "가족 구성원 수",
#         "생존률": "생존률",
#         "생존자수": "생존자 수",
#         "최대생존률": "최대 생존률 여부"
#     },
#     color_discrete_map={
#         True: "crimson",
#         False: "steelblue"
#     },
#     range_y=[0, 1]
# )


fig = px.scatter(
    family_stats,
    x="familysize",
    y="생존률",
    size="생존자수",
    color="최대생존률",
    title="가족 규모에 따른 생존률 산점도",
    labels={
        "familysize": "가족 구성원 수",
        "생존률": "생존률",
        "생존자수": "생존자 수",
        "최대생존률": "최대 생존률 여부"
    },
    color_discrete_map={
        True: "crimson",
        False: "steelblue"
    }
)

fig.update_traces(
    texttemplate="생존자 수: %{text}",
    textposition="outside",
    hovertemplate=
        "가족 구성원 수: %{x}<br>"
        "생존률: %{y:.2f}<br>"
        "생존자 수: %{text}명<br>"
        "<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)

# ===============================
# 숫자 표로 한 번 더 명확히 제시
# ===============================
st.subheader("📊 가족 규모별 생존 통계 (숫자)")

st.dataframe(
    family_stats.rename(columns={
        "familysize": "가족 구성원 수"
    }),
    use_container_width=True
)

# ===============================
# 분석 요약
# ===============================
st.subheader("📌 분석 요약 (세특 활용 가능)")
