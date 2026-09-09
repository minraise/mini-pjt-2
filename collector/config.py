import os
from dotenv import load_dotenv

load_dotenv()

# API
API_KEY = os.getenv("MOIS_API_KEY")
BASE_URL = "https://apis.data.go.kr/1741000/admmPpltnHhStus/selectAdmmPpltnHhStus" 

# 수집 대상 기간
TARGET_YMS = ["202605", "202606", "202607", "202608"]

# 서울 자치구 25개
SGG_CODES = {
    "1111000000": "종로구",
    "1114000000": "중구",
    "1117000000": "용산구",
    "1120000000": "성동구",
    "1121500000": "광진구",
    "1123000000": "동대문구",
    "1126000000": "중랑구",
    "1129000000": "성북구",
    "1130500000": "강북구",
    "1132000000": "도봉구",
    "1135000000": "노원구",
    "1138000000": "은평구",
    "1141000000": "서대문구",
    "1144000000": "마포구",
    "1147000000": "양천구",
    "1150000000": "강서구",
    "1153000000": "구로구",
    "1154500000": "금천구",
    "1156000000": "영등포구",
    "1159000000": "동작구",
    "1162000000": "관악구",
    "1165000000": "서초구",
    "1168000000": "강남구",
    "1171000000": "송파구",
    "1174000000": "강동구",
}

# 고정 파라미터
LV = "3"
NUM_OF_ROWS = 100
SLEEP_SEC = 0.3

# DB
DB_PATH = "data/warehouse.db"

FLOW_FILES = {
    '202605': {'zip': 'data/raw/250_LOCAL_RESD_ADMDONG_202605.zip', 'sep': ','},
    '202606': {'zip': 'data/raw/250_LOCAL_RESD_ADMDONG_202606.zip', 'sep': ','},
    '202607': {'zip': 'data/raw/250_LOCAL_RESD_ADMDONG_202607.zip', 'sep': ';'},
    '202608': {'zip': 'data/raw/250_LOCAL_RESD_ADMDONG_202608.zip', 'sep': ';'},
}

FLOW_COLS = ['base_date', 'hour', 'region_code', 'total_pop'] + [
    f'{g}_{b}' for g in ['male', 'female']
    for b in ['0_9', '10_14', '15_19', '20_24', '25_29', '30_34', '35_39',
              '40_44', '45_49', '50_54', '55_59', '60_64', '65_69', '70_over']
]

STORE_CSV = 'data/raw/소상공인시장진흥공단_상가_상권_정보_서울_202606.csv'