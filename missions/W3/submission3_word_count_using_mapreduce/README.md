## Wordcounting using MapReduce

### Funtional Requirements

- MapReduce 프로그램
    - ~~HDFS에서 입력 텍스트를 읽어야 함.~~
    - ~~Mapper는 각 단어의 Key-Value쌍을 Emit해야함.~~
    - ~~Reducer는 Mapper의 Emit Data를 활용하여 총 단어 수를 출력해야 함.~~
- 프로그램 실행
    - ~~MapReduce 작업이 Hadoop에서 오류없이 실행되어야 함~~
    - ~~E-book txt 파일을 활용하여 정확한 단어 수를 산출해야 함.~~
    - ~~Hadoop의 분산 처리 기능을 활용하여 효율적으로 처리해야 함.~~
- 결과 출력
    - ~~결과물은 HDFS에 저장된 txt 파일이어야 함.~~
    - ~~출력 파일에는 ‘\t’ or ‘ ‘으로 구분된 단어와 해당 개수가 포함되어야 함.~~
    - ~~출력은 HDFS에서 검색하고 읽을 수 있어야 함.~~

### Mapper

- Python Script를 활용하여 Mapper 클래스를 구현하고, 이를 활용하여 Map 작업을 수행합니다.
- e-book txt file을 한 줄씩 읽어와 {단어: 1}로 Key-Value mapping을 진행했습니다.
- 선택한 책은 Middlemarch이며, e-book txt file은 아래 링크에서 다운로드 받았습니다.

### Reducer

- Python Script를 활용하여 Reducer 클래스를 구현하고, 이를 활용하여 Reduce 작업을 수행합니다.
- Mapper의 결과를 받아와 wordcount 작업을 수행했습니다.
- 중간에 Sort를 해야하나 생각이 들었으나, 기본적으로 Hadoop에서 자동으로 Sort를 시켜줍니다.

### 실행 및 결과 확인

- `hdfs dfs -put ebook.txt /ebook`을 통해 파일을 업로드합니다.
    
    ![스크린샷 2024-07-19 오후 4.41.21.png](https://github.com/user-attachments/assets/a646ab61-0ac8-42a7-9e43-3e417b2e10a8)
    
- `ebook_wordcount.sh` 파일을 실행시켜 MapReduce 작업을 수행했습니다.
    
    ![Untitled](https://github.com/user-attachments/assets/29087856-3bd5-4b33-b017-bd5333b40a10)
    
- `hdfs dfs -ls /ebook_wordcount`를 활용하여 정상적으로 파일이 생성되었는지 확인했으며, Reduce.Job을 2로 설정했기에, 수행 결과 Partition이 두 개 생성됩니다.
    
    ![Untitled](https://github.com/user-attachments/assets/9e807e76-5ecf-4459-bd01-e4280bb917f0)
    
- `hdfs dfs -cat /ebook_wordcount/part-00001`를 통해결과 확인을 진행했습니다.
    
    ![스크린샷 2024-07-19 오후 4.36.54.png](https://github.com/user-attachments/assets/4f1d66c2-4ea9-4580-a9dc-b6055f75fb0a)


### Reference Link

- E-book Link: https://www.gutenberg.org/ebooks/145