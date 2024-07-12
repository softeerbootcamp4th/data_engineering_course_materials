# Learning Wiki

This repository is for organizing learning materials and week1'smissions.

## Contents

- [Missions](missions)
**wikipeida 페이지가 아닌, IMF 홈페이지에서 직접 데이터를 가져오는 방법**
![image](https://github.com/ssangmin-junior/softeer_wiki/assets/108651531/487d427a-38d2-4f6d-bb73-88b326166000)



[Report for Selected Countries and Subjects](https://www.imf.org/en/Publications/WEO/weo-database/2024/April/weo-report?c=512,914,612,171,614,311,213,911,314,193,122,912,313,419,513,316,913,124,339,638,514,218,963,616,223,516,918,748,618,624,522,622,156,626,628,228,924,233,632,636,634,238,662,960,423,935,128,611,321,243,248,469,253,642,643,939,734,644,819,172,132,646,648,915,134,652,174,328,258,656,654,336,263,268,532,944,176,534,536,429,433,178,436,136,343,158,439,916,664,826,542,967,443,917,544,941,446,666,668,672,946,137,546,674,676,548,556,678,181,867,682,684,273,868,921,948,943,686,688,518,728,836,558,138,196,278,692,694,962,142,449,564,565,283,853,288,293,566,964,182,359,453,968,922,714,862,135,716,456,722,942,718,724,576,936,961,813,726,199,733,184,524,361,362,364,732,366,144,146,463,528,923,738,578,537,742,866,369,744,186,925,869,746,926,466,112,111,298,927,846,299,582,487,474,754,698,&s=NGDPD,&sy=2022&ey=2029&ssm=0&scsm=1&scc=0&ssd=1&ssc=0&sic=0&sort=country&ds=.&br=1)

imf의 country,year 별 데이터를 스크랩 해와서 작업

→ https://github.com/ssangmin-junior/softeer_wiki/blob/main/missions/w1/etl/etl_as_imf.ipynb

**만약 데이터가 갱신되면 과거의 데이터는 어떻게 되어야 할까요? 과거의 데이터를 조회하는 게 필요하다면 ETL 프로세스를 어떻게 변경해야 할까요?**

**만약 데이터가 갱신되면 과거의 데이터는…**

1. 갱신될때마다 반기별 테이블 생성  하여 과거의 테이블을 따로 정리.
    
![image](https://github.com/ssangmin-junior/softeer_wiki/assets/108651531/4d1b7807-ff6f-4e37-b72e-9ff68edd23e9)

    

→ 나라별 GDP 데이터가 큰 데이터는 아니기 때문에 갱신될 때 반기마다 테이블이 생성되도 자원 사용에 크게 영향이 없어 하나의 데이터베이스에서 여러 테이블을 만듦.

![image](https://github.com/ssangmin-junior/softeer_wiki/assets/108651531/995b47a6-ce05-4ff3-a7d0-bed1374f27ad)

테이블 생성 할때 YEAR 컬럼 추가 (’2024-1’, ‘2024-2’ 형식)

데이터 삽입 할 때 현재 datetime 을 가지고 MMDD가 0701 전후로 YYYY-1, YYYY-2 구분 하여 삽입.

이미 YYYY-2이 이미 있는 경우 삽입 작업을 거치지 않음. (자원 절약) 

**과거의 데이터를 조회하는 게 필요하다면 ETL 프로세스를 어떻게 변경할까?**

테이블을 반기별로 생성하는 형식으로 했으므로 ETL 프로세스 변경없이 Analyze 부분에서 select문만 원하는 년도로 변경하면 된다.

'''
python
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()
query = f"""
SELECT * FROM Gdp2024_2
"""
```

https://github.com/ssangmin-junior/softeer_wiki/blob/main/missions/w1/ETL/GDP_year.py
