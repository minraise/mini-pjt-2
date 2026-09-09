import zipfile
import sqlite3 
import pandas as pd
import logging
from collector import config


def detect_sep(zf, info) -> str:
    with zf.open(info) as f:
        f.readline()
        first_data = f.readline().decode('cp949', errors='replace')
    return ';' if ';' in first_data else ','


def read_month(ym: str) -> pd.DataFrame:
    spec = config.FLOW_FILES[ym]
    dfs = []

    zf = zipfile.ZipFile(spec['zip'])
    for info in zf.infolist():
        sep = detect_sep(zf, info)
        with zf.open(info) as f:
            df = pd.read_csv(
                f,
                encoding='cp949',
                sep=sep,
                skiprows=1,
                names=config.FLOW_COLS,
                dtype=str,
            )
        dfs.append(df)

    result = pd.concat(dfs, ignore_index=True)
    logging.info(f"{ym} 읽기 완료: {len(result):,}행 (파일 {len(dfs)}개)")
    return result

def clean(df: pd.DataFrame) -> pd.DataFrame: 
    d = df.copy()


    # 행정동코드 공백 제거
    d['region_code'] = d['region_code'].str.strip()

    # 날짜 형식 변환: '20260801' → '2026-08-01'
    d['base_date'] = d['base_date'].str[:4] + '-' + d['base_date'].str[4:6] + '-' + d['base_date'].str[6:8]

    # 시간: '00' → 0
    d['hour'] = d['hour'].astype(int)

    # 마스킹(*)을 NULL로, 나머지는 숫자로
    num_cols = [c for c in config.FLOW_COLS if c not in ('base_date', 'hour', 'region_code')]
    for c in num_cols:
        d[c] = pd.to_numeric(d[c], errors='coerce')

    return d

def load_flow_pop(df: pd.DataFrame):
    """flow_pop_raw에 적재."""
    conn = sqlite3.connect(config.DB_PATH)
    
    cols = ', '.join(config.FLOW_COLS)
    placeholders = ', '.join(['?'] * len(config.FLOW_COLS))
    
    conn.executemany(
        f"INSERT OR REPLACE INTO flow_pop_raw ({cols}) VALUES ({placeholders})",
        df[config.FLOW_COLS].values.tolist()
    )
    conn.commit()
    conn.close()

def run():
    for ym in config.FLOW_FILES:
        df = clean(read_month(ym))
        load_flow_pop(df)
        logging.info(f"{ym} 적재 완료: {len(df):,}행")