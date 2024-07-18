# ETL learning

# Data flow
* Wiki -- extract to table data --> json | scraping
* json -- load as pandas obj(ram) --> print on console

# Advanced data flow
* Wiki -- extract to table data --> json | scraping,
* json -- transform to DB --> db
* db -- load as pandas obj(ram) --> print on console

* json file does a role as a temporary stored file.
* can refer 'The Solution' process in Week 1 script

## Feed back
데이터가 많으면 리스트를 쓸 수 없습니다. 메모리 공간이 감당 가능한 만큼 분리하여 적재해야합니다. 이 요구사항을 직접 구현하거나 DataFrame이 이 기능을 지원하므로 DataFrame을 잘 사용해야합니다...!

근데 왜 아직도 list를 쓰나요?
->
최적화가 가능한 상황(데이터가 적은 경우)를 제외하고 DataFrame을 사용하였습니다.

@dano-codesurfer
Member
dano-codesurfer commented 3 days ago
ETL중에서 Transform이 보이질 않습니다. 코드가 여기저기 뒤죽박죽으로 꼬여 있어요. 요구사항을 보면서 다시 정리해 보세요. 다시 PR 만들어서 올리세요.
->
Extract한 데이터와 기존에 준비된 데이터를 바탕으로 데이터를 변형하였습니다. string 에서 float로, million에서 billion단위로 바꾸었습니다.
요구사항을 만족시키기 위해 leftjoin한 데이터르 변형하여 필요한 컬럼은 남기고, 불필요한 컬럼은 제거하였습니다.
