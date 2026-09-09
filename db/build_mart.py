import sqlite3
import logging

DB_PATH = 'data/warehouse.db'

AGE_MAP = {
    'age_0_19':    ['0_9', '10_14', '15_19'],
    'age_20_29':   ['20_24', '25_29'],
    'age_30_49':   ['30_34', '35_39', '40_44', '45_49'],
    'age_50_64':   ['50_54', '55_59', '60_64'],
    'age_65_over': ['65_69', '70_over'],
}
GENDER_MAP = {'M': 'male', 'F': 'female'}


def build_region_monthly(conn):
    """지역 × 월 요약 마트."""
    conn.execute("DELETE FROM mart_region_monthly")
    conn.execute("""
        INSERT INTO mart_region_monthly
            (region_code, base_ym, avg_daily_pop, weekday_pop, weekend_pop,
             resident_pop, store_count, activity_ratio, pop_per_store)
        WITH flow AS (
            SELECT
                region_code,
                substr(base_date, 1, 7) AS base_ym,
                AVG(total_pop) AS avg_daily_pop,
                AVG(CASE WHEN strftime('%w', base_date) NOT IN ('0','6') THEN total_pop END) AS weekday_pop,
                AVG(CASE WHEN strftime('%w', base_date) IN ('0','6') THEN total_pop END) AS weekend_pop
            FROM flow_pop_raw
            GROUP BY region_code, base_ym
        ),
        stores AS (
            SELECT region_code, COUNT(*) AS store_count
            FROM store
            GROUP BY region_code
        )
        SELECT
            f.region_code,
            f.base_ym,
            f.avg_daily_pop,
            f.weekday_pop,
            f.weekend_pop,
            rp.total_pop,
            s.store_count,
            f.avg_daily_pop / rp.total_pop,
            f.avg_daily_pop / s.store_count
        FROM flow f
        JOIN resident_pop rp
          ON f.region_code = rp.region_code AND f.base_ym = rp.base_ym
        LEFT JOIN stores s
          ON f.region_code = s.region_code
    """)


def build_hourly_heatmap(conn):
    """지역 × 요일 × 시간대 마트 (4개월 전체 평균)."""
    conn.execute("DELETE FROM mart_hourly_heatmap")
    conn.execute("""
        INSERT INTO mart_hourly_heatmap (region_code, day_of_week, hour, avg_pop)
        SELECT
            region_code,
            CASE WHEN strftime('%w', base_date) = '0' THEN 7
                 ELSE CAST(strftime('%w', base_date) AS INTEGER)
            END AS day_of_week,
            hour,
            AVG(total_pop)
        FROM flow_pop_raw
        GROUP BY region_code, day_of_week, hour
    """)


def build_age_profile(conn):
    """지역 × 연령대 × 성별 마트."""

    blocks = []
    for band, parts in AGE_MAP.items():
        for gcode, gprefix in GENDER_MAP.items():
            cols = ' + '.join(f"COALESCE({gprefix}_{p}, 0)" for p in parts)
            blocks.append(f"""
                SELECT region_code, '{band}', '{gcode}', AVG({cols})
                FROM flow_pop_raw
                GROUP BY region_code
            """)
    query = "\nUNION ALL\n".join(blocks)

    conn.execute("DELETE FROM mart_age_profile")
    conn.execute(
        f"INSERT INTO mart_age_profile (region_code, age_band, gender, avg_pop) {query}"
    )


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    conn = sqlite3.connect(DB_PATH)

    build_region_monthly(conn)
    logging.info("mart_region_monthly 생성 완료")

    build_hourly_heatmap(conn)
    logging.info("mart_hourly_heatmap 생성 완료")

    build_age_profile(conn)
    logging.info("mart_age_profile 생성 완료")

    conn.commit()

    for t in ['mart_region_monthly', 'mart_hourly_heatmap', 'mart_age_profile']:
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        logging.info(f"{t}: {n:,}행")

    conn.close()


if __name__ == "__main__":
    main()