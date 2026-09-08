import plotly.express as px
import pandas as pd

DOW_LABELS = ['월', '화', '수', '목', '금', '토', '일']

def trend_chart(df: pd.DataFrame):
    """월별 평균 생활인구 추이 (선그래프)."""
    trend = df.groupby('base_ym')['avg_daily_pop'].mean().reset_index()

    fig = px.line(
        trend,
        x='base_ym',
        y='avg_daily_pop',
        markers=True,
        labels={
            'base_ym': '기준연월',
            'avg_daily_pop': '일평균 생활인구(명)',
        },
    )
    fig.update_layout(
        hovermode='x unified', 
        margin=dict(t=20),
    )
    return fig

def comparison_chart(df: pd.DataFrame, top_n: int = 15):
    """행정동별 점포당 생활인구 비교 (정렬된 가로 막대)."""
    avg = (
        df.groupby('dong_name')['pop_per_store']
        .mean()
        .reset_index()
        .sort_values('pop_per_store', ascending=True) 
        .tail(top_n)
    )

    fig = px.bar(
        avg,
        x='pop_per_store',
        y='dong_name',
        orientation='h',
        labels={
            'pop_per_store': '점포당 생활인구(명)',
            'dong_name': '행정동',
        },
    )
    fig.update_layout(margin=dict(t=20))
    return fig


def heatmap_chart(df: pd.DataFrame):
    """요일 × 시간대 생활인구 히트맵."""
    pivot = df.pivot(index='day_of_week', columns='hour', values='avg_pop')
    pivot.index = [DOW_LABELS[i - 1] for i in pivot.index]

    fig = px.imshow(
        pivot,
        labels=dict(x='시간대', y='요일', color='생활인구(명)'),
        aspect='auto',
        color_continuous_scale='YlOrRd',
    )
    fig.update_layout(margin=dict(t=20))
    return fig