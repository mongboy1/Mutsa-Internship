import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import openai

st.set_page_config(
    page_title="개인 지출 분석 대시보드",
    page_icon="💰",
    layout="wide"
)

st.title("💰 개인 지출 분석 대시보드")

# =========================
# 캐시 적용
# =========================
@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        try:
            df = pd.read_csv(file, encoding="utf-8")
        except:
            file.seek(0)
            df = pd.read_csv(file, encoding="cp949")
    else:
        df = pd.read_excel(file)
    return df


def preprocess_data(df):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["date", "amount"])
    df = df[df["amount"] > 0]
    df["description"] = df["description"].fillna("내역 없음")
    df["is_fixed"] = df["is_fixed"].fillna(False).astype(bool)
    return df


def generate_summary(df):
    total = df["amount"].sum()
    avg = df["amount"].mean()
    max_val = df["amount"].max()
    count = len(df)

    category_df = (
        df.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )

    category_df["percentage"] = (
        category_df["amount"] / total * 100
    ).round(1)

    return {
        "total": total,
        "avg": avg,
        "max": max_val,
        "count": count,
        "categories": category_df.to_dict("records")
    }


def generate_ai_insight(summary, api_key):
    openai.api_key = api_key.strip()

    prompt = f"""
총 지출: {summary['total']:,.0f}원
평균 지출: {summary['avg']:,.0f}원
최대 지출: {summary['max']:,.0f}원
거래 건수: {summary['count']}건
카테고리별 지출: {summary['categories']}

소비 패턴 분석과 절약 방법, 다음 달 예산 제안을 작성해주세요.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "당신은 전문 재무 컨설턴트입니다."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )

    return response.choices[0].message.content


def recommend_budget(summary):
    rows = []
    for cat in summary["categories"]:
        current = cat["amount"]
        recommended = int(current * 0.9)
        rows.append({
            "카테고리": cat["category"],
            "현재 지출": current,
            "권장 예산": recommended,
            "절약 가능 금액": current - recommended
        })
    return pd.DataFrame(rows)


def generate_report(summary, insight, budget_df):
    report = "# 📊 월간 지출 리포트\n\n"
    report += f"생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    report += f"- 총 지출: {summary['total']:,.0f}원\n"
    report += f"- 평균 지출: {summary['avg']:,.0f}원\n"
    report += f"- 최대 지출: {summary['max']:,.0f}원\n"
    report += f"- 거래 건수: {summary['count']}건\n\n"

    report += "## 카테고리 분석\n"
    for cat in summary["categories"]:
        report += f"- {cat['category']}: {cat['percentage']}% ({cat['amount']:,.0f}원)\n"

    report += "\n## AI 분석\n" + insight + "\n"

    report += "\n## 권장 예산\n"
    for _, row in budget_df.iterrows():
        report += f"- {row['카테고리']}: {row['권장 예산']:,.0f}원\n"

    return report


# =========================
# Sidebar 구조 개선
# =========================
with st.sidebar:

    st.header("📁 데이터")
    uploaded = st.file_uploader("CSV 또는 Excel 업로드", type=["csv", "xlsx"])

    st.divider()

    st.header("🤖 AI 설정")
    api_key = st.text_input("OpenAI API Key", type="password")

if uploaded:

    df = preprocess_data(load_data(uploaded))

    # =========================
    # 필터
    # =========================
    st.sidebar.divider()
    st.sidebar.header("🔎 필터")

    min_date = df["date"].min()
    max_date = df["date"].max()

    date_range = st.sidebar.date_input(
        "기간 선택",
        value=(min_date, max_date)
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[
            (df["date"].dt.date >= start_date) &
            (df["date"].dt.date <= end_date)
        ]

    categories = df["category"].unique().tolist()
    selected_categories = st.sidebar.multiselect(
        "카테고리 선택",
        categories,
        default=categories
    )

    df = df[df["category"].isin(selected_categories)]

    summary = generate_summary(df)

    tab1, tab2, tab3 = st.tabs(["📊 대시보드", "🤖 AI 분석", "📄 리포트"])

    # =========================
    # 대시보드
    # =========================
    with tab1:

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("총 지출", f"{summary['total']:,.0f}원")
        col2.metric("평균 지출", f"{summary['avg']:,.0f}원")
        col3.metric("최대 지출", f"{summary['max']:,.0f}원")
        col4.metric("거래 건수", f"{summary['count']}건")

        st.markdown("---")

        cat = df.groupby("category", as_index=False)["amount"].sum()

        fig_pie = px.pie(
            cat,
            values="amount",
            names="category",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        st.plotly_chart(fig_pie, use_container_width=True)

        df["year_month"] = df["date"].dt.strftime("%Y-%m")

        monthly = df.groupby("year_month", as_index=False)["amount"].sum()

        fig_line = px.line(
            monthly,
            x="year_month",
            y="amount",
            markers=True
        )

        st.plotly_chart(fig_line, use_container_width=True)

    # =========================
    # AI 분석
    # =========================
    with tab2:

        if st.button("AI 분석 실행"):

            if not api_key:
                st.warning("API Key를 입력하세요.")
            else:
                with st.spinner("AI 분석 중..."):
                    insight = generate_ai_insight(summary, api_key)
                    st.session_state["insight"] = insight
                    st.markdown(insight)

    # =========================
    # 리포트
    # =========================
    with tab3:

        if "insight" not in st.session_state:
            st.info("먼저 AI 분석을 실행하세요.")
        else:
            if st.button("리포트 생성"):
                with st.spinner("리포트 생성 중..."):

                    budget_df = recommend_budget(summary)
                    report = generate_report(
                        summary,
                        st.session_state["insight"],
                        budget_df
                    )

                    st.markdown(report)

                    st.download_button(
                        "리포트 다운로드 (Markdown)",
                        report,
                        "monthly_expense_report.md"
                    )

else:
    st.info("왼쪽 사이드바에서 파일을 업로드하세요.")
