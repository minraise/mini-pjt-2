# API 응답
import pandas as pd 
kik = pd.read_excel('data/raw/KIKcd_H.20260720.xlsx')

sgg = kik[(kik['시도명']=='서울특별시') & (kik['시군구명'].notna()) & (kik['읍면동명'].isna())]

print(len(sgg))
print(sgg[['행정동코드', '시군구명']].to_string())

for _, row in sgg.iterrows():
    print(f'    "{row["행정동코드"]}": "{row["시군구명"]}",')