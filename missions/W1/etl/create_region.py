import sqlite3

"""
국가,대륙 정보를 가지고 있는 region.txt 파일을 얼어
국가,대륙 정보를 가지고 있는 테이블 CONTINENT를 생성한 후
GDP, CONTINENT 테이블을 LEFT JOIN한 테이블 GDP_CONTI을 생성하는 함수
국가,대륙 쌍은 데이터의 크기가 크지 않으므로 list 자료형을 사용하여 성능 저하를 최소화
"""
def create_nation_conti_table():
    txt_file = './region.txt'
    nation_conti_list = []
    with open(txt_file, mode='r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # 줄 바꿈 문자 제거
            if line:
                nation, continent = line.split(',')
                nation_conti_list.append((nation, continent))
    
    with sqlite3.connect('World_Economies.db') as conn:
        cur = conn.cursor()
        cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS CONTINENT (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nation TEXT UNIQUE,
                continent TEXT
                )
                '''
        )
        
        for item in nation_conti_list:
            try:
                cur.execute(
                    '''
                    INSERT INTO CONTINENT (nation, continent) VALUES (?, ?)
                    ''',
                    (item[0], item[1])
                )
            except sqlite3.IntegrityError as e:
                print(e)
                break
            
create_nation_conti_table()