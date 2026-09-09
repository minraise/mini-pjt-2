import sqlite3, pandas as pd

AGE_MAP = {
    'age_0_19':    ['0_9', '10_14', '15_19'],
    'age_20_29':   ['20_24', '25_29'],
    'age_30_49':   ['30_34', '35_39', '40_44', '45_49'],
    'age_50_64':   ['50_54', '55_59', '60_64'],
    'age_65_over': ['65_69', '70_over'],
}
GENDER_MAP = {'M': 'male', 'F': 'female'}

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

conn = sqlite3.connect('data/warehouse.db')
conn.execute("DELETE FROM mart_age_profile")
conn.execute(f"INSERT INTO mart_age_profile (region_code, age_band, gender, avg_pop) {query}")
conn.commit()

print(pd.read_sql_query("SELECT COUNT(*) AS n FROM mart_age_profile", conn))
conn.close()