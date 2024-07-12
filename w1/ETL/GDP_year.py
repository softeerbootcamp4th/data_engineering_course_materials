import pandas as pd
import sqlite3
from datetime import datetime
import os

df = pd.read_csv('region.csv')
df = df[['Country', 'GDP_USD_billions', 'Region']]   

# 현재 날짜 확인
now = datetime.now()
current_year = now.year
half_year = '_1' if now.month < 7 or (now.month == 7 and now.day == 1) else '_2'
current_period = f"Gdp{current_year}{half_year}"

db_filename = 'gdp.db'
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# 테이블 생성
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {current_period} (
    Country TEXT PRIMARY KEY,
    GDP_USD_billion REAL,
    YEAR TEXT
)
''')

# YYYY-2 데이터가 있는지 확인
cursor.execute(f'''
SELECT COUNT(*)
FROM {current_period}
WHERE YEAR = ?
''', (f"{current_year}_2",))
count = cursor.fetchone()[0]

# YYYY-2 데이터가 없는 경우에 데이터 삽입
if count == 0:
    for _, row in df.iterrows():
        cursor.execute(f'''
        INSERT OR REPLACE INTO {current_period} (Country, GDP_USD_billion, YEAR)
        VALUES (?, ?, ?)
        ''', (row['Country'], row['GDP_USD_billions'], current_period[3:]))

print(f"데이터베이스 저장 {db_filename}")

conn.commit()
conn.close()

conn = sqlite3.connect(db_filename)
cursor = conn.cursor()
query = f"""
SELECT * FROM Gdp2024_2
"""

df = pd.read_sql_query(query, conn)
display(df)

conn.close()
