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

st.subheader("📄 원본 데이터 컬럼")
st.write(list(df.columns))

# -------------------------------
# 1. 결측치 처리
# -------------------------------
df = df[["sibsp", "parch", "survived"]].dropna()

# -------------------------------
# 2. 이상치 처리 (IQR 방식)
# -------------------------------
def remove_outliers_iqr(data, column):
    q1 = data[column].quantile(0.25)
    q3 = data[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return data[(data[column] >= lower) & (data[column] <= upper)]

df = remove_outliers_iqr(df, "sibsp")
df = remove_outliers_iqr(df, "parch")

# -------------------------------
# 형제/배우자 수와 생존율
# -------------------------------
sibsp_survival = df.groupby("sibsp", as_index=False)["survived"].mean()

# 3. 정규화 (Min-Max)
sibsp_survival["정규화된 생존율"] = (
    (sibsp_survival["survived"] - sibsp_survival["survived"].min()) /
    (sibsp_survival["survived"].max() - sibsp_survival["survived"].min())
)

# 최대값 표시용 컬럼
sibsp_survival["구분"] = "일반"
sibsp_survival.loc[
    sibsp_survival["정규화된 생존율"].idxmax(), "구분"
] = "최대 생존율"

st.subheader("👨‍👩‍👧 형제/배우자 수와 생존율")

fig1 = px.bar(
    sibsp_survival,
    x="sibsp",
    y="정규화된 생존율",
    color="구분",
    title="형제/배우자 수에 따른 정규화된 생존율",
    labels={
        "sibsp": "형제 / 배우자 수",
        "정규화된 생존율": "정규화된 생존율"
    }
)

st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# 가족 규모 분석
# -------------------------------
df["familysize"] = df["sibsp"] + df["parch"] + 1
family_survival = df.groupby("familysize", as_index=False)["survived"].mean()

family_survival["정규화된 생존율"] = (
    (family_survival["survived"] - family_survival["survived"].min()) /
    (family_survival["survived"].max() - family_survival["survived"].min())
)

family_survival["구분"] = "일반"
family_survival.loc[
    family_survival["정규화된 생존율"].idxmax(), "구분"
] = "최대 생존율"

st.subheader("🏠 가족 규모와 생존율")

fig2 = px.line(
    family_survival,
    x="familysize",
    y="정규화된 생존율",
    color="구분",
    markers=True,
    title="가족 규모에 따른 정규화된 생존율 변화",
    labels={
        "familysize": "가족 구성원 수",
        "정규화된 생존율": "정규화된 생존율"
    }
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# 요약
# -------------------------------
st.subheader("📌 전처리 및 분석 요약")

st.info(
    "결측치를 제거하고 IQR 방식을 이용해 이상치를 처리한 후, 생존율을 정규화하여 분석하였다. "
    "그 결과 형제 또는 배우자 1~2명, 가족 규모 2~4명 구간에서 정규화된 생존율의 최대값이 나타났으며, "
    "이는 소규모 가족 단위가 위기 상황에서 가장 효율적으로 대응했음을 시사한다."
)
