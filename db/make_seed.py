import pandas as pd
import random

random.seed(42)

# 상수
YMS = ['2026-05', '2026-06', '2026-07', '2026-08']

# 시간대별 배율 (0시~23시)
HOUR_FACTOR = [
    0.3, 0.25, 0.2, 0.2, 0.25, 0.4,      # 0~5시
    0.5, 0.55, 0.7, 0.8, 0.9, 1.0,       # 6~11시
    1.2, 1.3, 1.35, 1.4, 1.5, 1.4,       # 12~17시
    1.2, 1.1, 1.0, 0.8, 0.5, 0.4,        # 18~23시
]

# 요일 배율 (인덱스 0=월 ... 6=일)
DOW_FACTOR = [1.05, 1.05, 1.05, 1.05, 1.1, 0.9, 0.85]

# 연령대 구성비 (합 1.0)
AGE_FACTOR = {
    'age_0_19':    0.13,
    'age_20_29':   0.15,
    'age_30_49':   0.30,
    'age_50_64':   0.23,
    'age_65_over': 0.19,
}
AGE_BANDS = list(AGE_FACTOR.keys())
GENDERS = ['M', 'F']

# 데이터 누락 테스트용
MISSING_CODE = '11110540'
MISSING_YM = '2026-08'


# 대상 행정동 20개
kik = pd.read_excel('data/raw/KIKcd_H.20260720.xlsx')
dong = kik[(kik['시도명'] == '서울특별시') & (kik['읍면동명'].notna())].head(20)

lines = []


# 1. region
for _, row in dong.iterrows():
    code = str(row['행정동코드'])[:8]
    lines.append(
        f"INSERT INTO region VALUES "
        f"('{code}', '서울특별시', '{row['시군구명']}', '{row['읍면동명']}');"
    )


# 2. mart_region_monthly
for _, row in dong.iterrows():
    code = str(row['행정동코드'])[:8]
    resident = random.randint(2000, 30000)
    store_cnt = random.randint(200, 5000)
    base_ratio = random.uniform(0.5, 5.0)

    for ym in YMS:
        # 누락 테스트
        if code == MISSING_CODE and ym == MISSING_YM:
            continue

        ratio = base_ratio * random.uniform(0.9, 1.1)
        avg_pop = resident * ratio
        weekday = avg_pop * random.uniform(1.0, 1.2)
        weekend = avg_pop * random.uniform(0.7, 1.0)
        activity_ratio = avg_pop / resident
        pop_per_store = avg_pop / store_cnt

        lines.append(
            f"INSERT INTO mart_region_monthly VALUES "
            f"('{code}', '{ym}', {avg_pop:.2f}, {weekday:.2f}, {weekend:.2f}, "
            f"{resident}, {store_cnt}, {activity_ratio:.3f}, {pop_per_store:.2f});"
        )


# 3. mart_hourly_heatmap
for _, row in dong.iterrows():
    code = str(row['행정동코드'])[:8]
    base_pop = random.randint(4000, 135000)

    for dow in range(1, 8):          # 1=월 ~ 7=일
        for hour in range(24):       # 0~23
            avg_pop = (
                base_pop
                * HOUR_FACTOR[hour]
                * DOW_FACTOR[dow - 1]
                * random.uniform(0.95, 1.05)
            )

            # 마스킹 재현: 새벽 시간대 일부는 NULL
            if hour < 5 and random.random() < 0.1:
                value_str = "NULL"
            else:
                value_str = f"{avg_pop:.2f}"

            lines.append(
                f"INSERT INTO mart_hourly_heatmap VALUES "
                f"('{code}', {dow}, {hour}, {value_str});"
            )


# 4. mart_age_profile
for _, row in dong.iterrows():
    code = str(row['행정동코드'])[:8]
    base_pop = random.randint(4000, 135000)

    for band in AGE_BANDS:
        for gender in GENDERS:
            avg_pop = base_pop * AGE_FACTOR[band] * 0.5 * random.uniform(0.95, 1.05)
            lines.append(
                f"INSERT INTO mart_age_profile VALUES "
                f"('{code}', '{band}', '{gender}', {avg_pop:.2f});"
            )


# 파일 저장
with open('db/seed_dummy.sql', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

from collections import Counter
print(Counter(l.split()[2] for l in lines))
print(f'{len(lines)}개 INSERT 생성')