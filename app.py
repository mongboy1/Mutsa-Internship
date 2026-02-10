
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="개인 지출 분석 대시보드",
    page_icon="💰",
    layout="wide"
)

st.title("💰 개인 지출 분석 대시보드")

with st.sidebar:
    st.header("📁 데이터 업로드")
    uploaded_file = st.file_uploader(
        "CSV 또는 Excel 파일을 업로드하세요",
        type=["csv", "xlsx", "xls"]
    )

def load_and_preprocess(file):
    if file.name.endswith(".csv"):
        try:
            df = pd.read_csv(file, encoding="utf-8")
        except UnicodeDecodeError:
            file.seek(0)
            df = pd.read_csv(file, encoding="cp949")
    else:
        df = pd.read_excel(file)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df = df[df["amount"] > 0]

    valid_categories = [
        "식비", "교통비", "카페", "쇼핑",
        "주거/통신", "구독", "의료/건강",
        "문화/여가", "교육", "기타"
    ]
    df["category"] = df["category"].where(df["category"].isin(valid_categories), "기타")
    df["description"] = df["description"].fillna("내역 없음")
    df["is_fixed"] = df["is_fixed"].fillna(False).astype(bool)
    df["year_month"] = df["date"].dt.strftime("%Y-%m")

    return df

if uploaded_file is not None:
    try:
        df = load_and_preprocess(uploaded_file)
        st.success(f"데이터 로드 완료: {len(df)}건")

        with st.sidebar:
            st.header("🔍 필터")

            min_date = df["date"].min()
            max_date = df["date"].max()

            date_range = st.date_input(
                "기간 선택",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )

            categories = df["category"].unique().tolist()
            selected_categories = st.multiselect(
                "카테고리 선택",
                options=categories,
                default=categories
            )

        df_filtered = df.copy()

        if len(date_range) == 2:
            start_date, end_date = date_range
            df_filtered = df_filtered[
                (df_filtered["date"].dt.date >= start_date) &
                (df_filtered["date"].dt.date <= end_date)
            ]

        if selected_categories:
            df_filtered = df_filtered[df_filtered["category"].isin(selected_categories)]
        else:
            df_filtered = df_filtered.iloc[0:0]

        if df_filtered.empty:
            st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
        else:
            st.markdown("## 📊 핵심 지표 (KPI)")
            col1, col2, col3, col4 = st.columns(4)

            col1.metric("총 지출", f"{df_filtered['amount'].sum():,.0f} 원")
            col2.metric("평균 지출", f"{df_filtered['amount'].mean():,.0f} 원")
            col3.metric("최대 지출", f"{df_filtered['amount'].max():,.0f} 원")
            col4.metric("거래 건수", f"{len(df_filtered)} 건")

            st.markdown("---")

            col_left, col_right = st.columns(2)

            with col_left:
                st.markdown("### 🥧 카테고리별 지출 비율")
                category_sum = df_filtered.groupby("category")["amount"].sum().reset_index()
                fig_pie = px.pie(category_sum, values="amount", names="category", hole=0.4)
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_right:
                st.markdown("### 📈 월별 지출 추이")
                monthly_sum = (
                    df_filtered.groupby("year_month")["amount"]
                    .sum()
                    .reset_index()
                    .sort_values("year_month")
                )
                fig_line = px.line(monthly_sum, x="year_month", y="amount", markers=True)
                st.plotly_chart(fig_line, use_container_width=True)

            with st.expander("📋 전처리된 데이터 미리보기"):
                st.dataframe(df_filtered.head(20))

    except Exception as e:
        st.error(f"처리 중 오류가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에서 CSV 또는 Excel 파일을 업로드하세요.")
