import sqlite3
import logging
from collector import config


def load(resident_rows: list, region_rows: list):
    """변환된 데이터를 DB에 적재."""
    conn = sqlite3.connect(config.DB_PATH)

    conn.executemany(
        "INSERT OR REPLACE INTO resident_pop (region_code, base_ym, total_pop, hh_cnt) "
        "VALUES (?, ?, ?, ?)",
        resident_rows
    )

    conn.executemany(
        "INSERT OR REPLACE INTO region (region_code, sido_name, sigungu_name, dong_name) "
        "VALUES (?, ?, ?, ?)",
        region_rows
    )

    conn.commit()

    # 적재 검증
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM resident_pop")
    logging.info(f"resident_pop 적재 완료: {cur.fetchone()[0]}행")
    cur.execute("SELECT COUNT(*) FROM region")
    logging.info(f"region 적재 완료: {cur.fetchone()[0]}행")

    conn.close()