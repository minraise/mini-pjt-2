import pandas as pd
import sqlite3

DB_PATH = "data/warehouse.db"


def load_region_monthly(sigungu: str, ym_from: str, ym_to: str) -> pd.DataFrame:
    """자치구 + 기간으로 행정동별 월간 지표를 조회."""
    with sqlite3.connect(DB_PATH) as con:
        q = """
            SELECT
                r.dong_name,
                m.region_code,
                m.base_ym,
                m.avg_daily_pop,
                m.weekday_pop,
                m.weekend_pop,
                m.resident_pop,
                m.store_count,
                m.activity_ratio,
                m.pop_per_store
            FROM mart_region_monthly m
            JOIN region r ON m.region_code = r.region_code
            WHERE r.sigungu_name = ?
              AND m.base_ym BETWEEN ? AND ?
            ORDER BY m.base_ym, r.dong_name
        """
        return pd.read_sql(q, con, params=(sigungu, ym_from, ym_to))

def load_hourly_heatmap(region_code: str) -> pd.DataFrame:
    """특정 행정동의 요일 × 시간대 생활인구 (168행)."""
    with sqlite3.connect(DB_PATH) as con:
        q = """
            SELECT
                day_of_week,
                hour,
                avg_pop
            FROM mart_hourly_heatmap
            WHERE region_code = ?
            ORDER BY day_of_week, hour
        """
        return pd.read_sql(q, con, params=(region_code,))


def load_age_profile(region_code: str) -> pd.DataFrame:
    """특정 행정동의 연령대 × 성별 생활인구 (10행)."""
    with sqlite3.connect(DB_PATH) as con:
        q = """
            SELECT
                age_band,
                gender,
                avg_pop
            FROM mart_age_profile
            WHERE region_code = ?
            ORDER BY age_band, gender
        """
        return pd.read_sql(q, con, params=(region_code,))


def load_filter_options() -> pd.DataFrame:
    """사이드바 필터용 자치구·행정동 목록."""
    with sqlite3.connect(DB_PATH) as con:
        q = """
            SELECT
                region_code,
                sigungu_name,
                dong_name
            FROM region
            ORDER BY sigungu_name, dong_name
        """
        return pd.read_sql(q, con)