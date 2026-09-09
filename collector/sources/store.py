import sqlite3
import logging
import pandas as pd
from collector import config


def read_store() -> pd.DataFrame:
    df = pd.read_csv(
        config.STORE_CSV,
        encoding='utf-8',
        usecols=['상가업소번호', '행정동코드', '상권업종중분류명'],
        dtype=str,
    )
    df = df.rename(columns={
        '상가업소번호': 'store_id',
        '행정동코드': 'region_code',
        '상권업종중분류명': 'category_m',
    })
    logging.info(f"상가 읽기 완료: {len(df):,}행")
    return df


def load_store(df: pd.DataFrame):
    conn = sqlite3.connect(config.DB_PATH)
    conn.executemany(
        "INSERT OR REPLACE INTO store (store_id, region_code, category_m) VALUES (?, ?, ?)",
        df[['store_id', 'region_code', 'category_m']].values.tolist()
    )
    conn.commit()
    conn.close()
    logging.info(f"store 적재 완료: {len(df):,}행")


def run():
    load_store(read_store())