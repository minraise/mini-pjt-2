import streamlit as st
import pandas as pd
from app.charts import trend_chart, comparison_chart, heatmap_chart, age_chart

from app.repository import (
    load_region_monthly,
    load_hourly_heatmap,
    load_age_profile,
    load_filter_options,
)

st.set_page_config(page_title="서울 상권 지원 대상 대시보드", layout="wide")


# 사이드바 — 필터
options = load_filter_options()

with st.sidebar:
    st.header("필터")

    sigungu = st.selectbox(
        "자치구",
        sorted(options["sigungu_name"].unique())
    )

    # 선택한 자치구에 속한 동만 추리기
    dong_options = options[options["sigungu_name"] == sigungu]

    dong_name = st.selectbox(
        "행정동 (상세 분석용)",
        sorted(dong_options["dong_name"].unique())
    )

    # 선택한 동의 region_code 찾기
    region_code = dong_options[
        dong_options["dong_name"] == dong_name
    ]["region_code"].iloc[0]

    ym_from, ym_to = st.select_slider(
        "기간",
        options=["2026-05", "2026-06", "2026-07", "2026-08"],
        value=("2026-05", "2026-08"),
    )


# 데이터 조회
df = load_region_monthly(sigungu, ym_from, ym_to)

# 빈 결과 처리
if df.empty:
    st.warning(f"{sigungu}의 {ym_from}~{ym_to} 데이터가 없습니다.")
    st.stop()


# 결론 문장 (Day 5에 실데이터 보고 확정)
st.title("TODO: 결론 한 줄")
st.caption(f"기준: {ym_from} ~ {ym_to} · 출처: 서울 생활인구, 행정안전부 주민등록인구, 소상공인시장진흥공단")


# KPI 4개
c1, c2, c3, c4 = st.columns(4)

avg_ratio = df['activity_ratio'].mean()
avg_pop_per_store = df['pop_per_store'].mean()

c1.metric("평균 주간활동 배율", f"{avg_ratio:.2f}")
c2.metric("평균 점포당 생활인구", f"{avg_pop_per_store:.1f}명")

dong_avg = df.groupby('dong_name')[['activity_ratio', 'pop_per_store']].mean()
candidates = dong_avg[
    (dong_avg['activity_ratio'] > avg_ratio) & (dong_avg['pop_per_store'] > avg_pop_per_store)
]
c3.metric("지원 대상 후보", f"{len(candidates)}개 동")

yms = sorted(df['base_ym'].unique())
if len(yms) >= 2:
    last_pop = df[df['base_ym'] == yms[-1]]['avg_daily_pop'].mean()
    prev_pop = df[df['base_ym'] == yms[-2]]['avg_daily_pop'].mean()
    change = (last_pop - prev_pop) / prev_pop
    c4.metric("전월 대비 생활인구", f"{last_pop:,.0f}명", delta=f"{change:+.1%}")
else:
    c4.metric("전월 대비 생활인구", "비교 불가")



# 탭 3개
tab1, tab2, tab3 = st.tabs(["상황: 추이", "문제: 동별 비교", "근거: 상세"])

with tab1:
    st.subheader(f"{sigungu} 생활인구 추이")
    st.plotly_chart(trend_chart(df), use_container_width=True)
    st.caption("이 차트는 선택한 자치구의 월별 평균 생활인구 변화를 보여줍니다.")

with tab2:
    st.subheader("행정동별 점포당 생활인구")
    st.plotly_chart(comparison_chart(df), use_container_width=True)
    st.caption("값이 클수록 점포 하나가 감당하는 생활인구가 많다는 뜻으로, 수요 대비 공급이 부족한 상태를 시사합니다.")

with tab3:
    st.subheader(f"{dong_name} 상세")
    heatmap_df = load_hourly_heatmap(region_code)
    age_df = load_age_profile(region_code)

    if heatmap_df.empty:
        st.info(f"{dong_name}의 시간대별 데이터가 없습니다.")
    else:
        st.plotly_chart(heatmap_chart(heatmap_df), use_container_width=True)
        st.caption("색이 진할수록 그 시간대에 사람이 많다는 뜻입니다.")

        st.plotly_chart(age_chart(age_df), use_container_width=True)
        st.caption("이 동에 머무는 사람들의 연령·성별 구성입니다.")