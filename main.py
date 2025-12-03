# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io
from typing import Optional

st.set_page_config(page_title="운동 데이터 분석", layout="wide")

st.title("🏃‍♂️ 운동 데이터 상관성 분석")
st.write("체지방율(Body Fat)과 상관관계가 높은 속성을 찾아 산점도와 히트맵으로 시각화합니다.")

# --- Helper functions ---
def load_default_file(path="/mnt/data/fitness data.xlsx") -> Optional[pd.DataFrame]:
    try:
        df = pd.read_excel(path)
        return df
    except Exception:
        return None

def smart_find_bodyfat_col(df: pd.DataFrame):
    """
    체지방율 컬럼을 자동으로 찾음.
    검색 키워드들(bodyfat, body_fat, 체지방, 체지방율 등)을 체크.
    Returns column name or None.
    """
    candidates = []
    keywords = ["체지방율", "체지방", "체지방률", "bodyfat", "body_fat", "body fat", "body_fat_pct", "fat"]
    cols = df.columns.astype(str)
    for c in cols:
        low = c.lower()
        for kw in keywords:
            if kw.replace(" ", "").lower() in low.replace(" ", ""):
                candidates.append(c)
                break
    # If multiple, prefer exact matches
    if len(candidates) == 0:
        return None
    if len(candidates) == 1:
        return candidates[0]
    # prefer the one containing 'rate' or '율' etc.
    priority_keys = ["체지방율", "체지방", "bodyfat", "body_fat", "body fat", "fat"]
    for pk in priority_keys:
        for c in candidates:
            if pk.replace(" ", "").lower() in c.lower().replace(" ", ""):
                return c
    return candidates[0]

def prepare_numeric_df(df: pd.DataFrame):
    # 선택 가능한 숫자형 컬럼만 골라 결측치를 처리
    numeric = df.select_dtypes(include=[np.number]).copy()
    if numeric.shape[1] == 0:
        # attempt to coerce columns to numeric
        for col in df.columns:
            coerced = pd.to_numeric(df[col], errors="coerce")
            if coerced.notna().sum() > 0:
                numeric[col] = coerced
    return numeric

# --- UI: load data ---
st.sidebar.header("데이터 불러오기")
st.sidebar.write("아래 중 선택:")
uploaded = st.sidebar.file_uploader("엑셀(.xlsx/.xls) 또는 CSV 파일 업로드", type=["xlsx","xls","csv"])
use_default = False
df = None
if uploaded is not None:
    try:
        if uploaded.name.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded)
        else:
            df = pd.read_csv(uploaded)
        st.sidebar.success(f"업로드 완료: {uploaded.name}")
    except Exception as e:
        st.sidebar.error(f"파일 로드 실패: {e}")

# if no upload, attempt to load default path (useful when running on local server that has file)
if df is None:
    df = load_default_file()
    if df is not None:
        use_default = True
        st.sidebar.info("기본 경로의 'fitness data.xlsx' 파일을 사용합니다.")
    else:
        st.sidebar.warning("기본 파일이 없습니다. 업로드 해주세요.")
        st.stop()

st.write("### 데이터 미리보기")
st.dataframe(df.head(100))

# Find body fat column automatically, allow override
detected = smart_find_bodyfat_col(df)
st.sidebar.header("분석 설정")
bodyfat_col = st.sidebar.text_input("체지방(체지방율) 컬럼명 (자동 탐지 가능):", value=detected or "")
if bodyfat_col == "":
    st.sidebar.warning("체지방 컬럼명을 입력하거나 자동 탐지를 확인하세요.")
    st.stop()
if bodyfat_col not in df.columns:
    st.error(f"선택한 컬럼 '{bodyfat_col}'가 데이터에 없습니다. 열 이름을 정확히 입력하세요.")
    st.stop()

# Prepare numeric dataframe and compute correlations
numeric_df = prepare_numeric_df(df)
if bodyfat_col not in numeric_df.columns:
    # try coercion
    numeric_df[bodyfat_col] = pd.to_numeric(df[bodyfat_col], errors="coerce")

# Drop columns with all NaN
numeric_df = numeric_df.loc[:, numeric_df.notna().any()].copy()
# Drop rows where bodyfat is NaN
numeric_df = numeric_df[numeric_df[bodyfat_col].notna()].copy()
if numeric_df.shape[0] < 5:
    st.error("분석할 충분한 숫자 데이터가 없습니다 (행이 너무 적음).")
    st.stop()

st.write(f"분석에 사용된 수치형 컬럼: {list(numeric_df.columns)}")
corr = numeric_df.corr(method='pearson')
# Correlations with bodyfat
body_corr = corr[bodyfat_col].drop(labels=[bodyfat_col]).dropna()
if body_corr.empty:
    st.warning("체지방과 상관계수를 계산할 수 있는 다른 수치형 컬럼이 없습니다.")
    st.stop()

# Rank by absolute correlation
ranked = body_corr.abs().sort_values(ascending=False)
top_k = st.sidebar.slider("상관관계 상위 몇 개의 속성을 보여줄까요?", min_value=1, max_value=min(10, len(ranked)), value=min(3, len(ranked)))
top_features = ranked.head(top_k).index.tolist()

st.write("## 🔍 체지방과 상관관계 높은 속성 (절대값 기준)")
res_df = pd.DataFrame({
    "feature": body_corr.index,
    "pearson_corr": body_corr.values,
    "abs_corr": np.abs(body_corr.values)
}).sort_values("abs_corr", ascending=False).reset_index(drop=True)
st.dataframe(res_df.head(20))

# Scatter plots for top features
st.write("## 📈 산점도 (체지방 vs 상위 속성)")
cols = st.columns(max(1, top_k))
for i, feat in enumerate(top_features):
    with cols[i % max(1, top_k)]:
        st.subheader(f"{feat} (상관계수: {body_corr[feat]:.3f})")
        fig = px.scatter(numeric_df, x=feat, y=bodyfat_col, trendline="ols",
                         labels={feat: feat, bodyfat_col: bodyfat_col},
                         title=f"{bodyfat_col} vs {feat}")
        st.plotly_chart(fig, use_container_width=True)

# Correlation heatmap for numeric columns
st.write("## 🔥 수치형 변수 상관계수 히트맵")
# Reorder columns to put bodyfat first
cols_for_heat = [bodyfat_col] + [c for c in numeric_df.columns if c != bodyfat_col]
corr_subset = numeric_df[cols_for_heat].corr()
# Plotly heatmap
fig_hm = go.Figure(data=go.Heatmap(
    z=corr_subset.values,
    x=corr_subset.columns,
    y=corr_subset.index,
    zmin=-1, zmax=1,
    colorbar=dict(title="Pearson r")
))
fig_hm.update_layout(width=900, height=700, title="상관계수 히트맵 (Pearson r)")
st.plotly_chart(fig_hm, use_container_width=True)

# 상세: 선택한 특성의 분포와 상관분석 정보
st.write("## 상세 분석 도구")
selected_feature = st.selectbox("산점도/상세 보기: 특성 선택", options=cols_for_heat, index=1 if len(cols_for_heat)>1 else 0)
if selected_feature:
    st.write(f"### {selected_feature}와 {bodyfat_col}의 관계")
    fig2 = px.scatter(numeric_df, x=selected_feature, y=bodyfat_col, trendline="ols",
                      labels={selected_feature: selected_feature, bodyfat_col: bodyfat_col},
                      title=f"{bodyfat_col} vs {selected_feature}")
    st.plotly_chart(fig2, use_container_width=True)

    # 간단한 통계
    st.write("기본 통계:")
    st.write(numeric_df[[selected_feature, bodyfat_col]].describe())

    # 회귀계수/통계
    try:
        # 추세선 결과 얻기
        res = px.get_trendline_results(px.scatter(numeric_df, x=selected_feature, y=bodyfat_col, trendline="ols"))
        model = res.iloc[0]["px_fit_results"]
        coef = model.params
        st.write("회귀 계수 (OLS):")
        st.write(coef)
        st.write("회귀 요약 (요약 통계):")
        st.text(model.summary().as_text())
    except Exception:
        st.info("회귀 요약을 계산할 수 없었습니다.")

st.write("---")
st.caption("앱: 업로드된 엑셀/CSV 파일에서 수치형 데이터를 자동 추출하여 체지방과의 Pearson 상관관계를 계산합니다. 필요하면 분석 전 데이터 전처리를 해주세요.")
