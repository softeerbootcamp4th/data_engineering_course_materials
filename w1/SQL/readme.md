<img width="407" alt="image" src="https://github.com/ssangmin-junior/softeer_wiki/assets/108651531/7f50d05c-8645-45d9-8159-b456f82c4cee">
위와 같이 숫자 데이터가 정수형 타입에 담겨있지 않은 상황일 때 
<img width="535" alt="image" src="https://github.com/ssangmin-junior/softeer_wiki/assets/108651531/49c3aba5-526e-4bbe-9d93-9649a0b5f16c">
이러한 코드를 실행하게 되면  다음과 같이 출력되어야 하지만 1,2,3,4 같이 첫자리가 5보다 작은경우 출력결과물에 포함되는 케이스가 있음.
<img width="936" alt="image" src="https://github.com/ssangmin-junior/softeer_wiki/assets/108651531/a9295e98-b9c7-4eda-a93d-2a7a75eb812c">

팀과의 회의를 통해 오류를 찾고 해결책을 모색 하였음. 
데이터를 불러들이는 과정에서의 오류로 판단되어 데이터를 읽을 때 숫자가 담긴 컬럼의 데이터 타입을 정수형으로 지정 해주어 오류 해결하였음.
