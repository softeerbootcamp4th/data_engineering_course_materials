[강의(월)]
[강의(금)]

## W2. 마스터 스택

### Docker는 언제 왜 쓰나요? Big Data와는 어떤 연관이 있나요?

**Docker 사용 시기와 이유:**

- **환경 일관성 보장**: Docker를 사용하면 애플리케이션과 모든 종속성을 컨테이너에 패키징하여 일관된 실행 환경을 제공합니다. 이는 개발, 테스트, 배포 과정에서 환경 차이로 인한 문제를 최소화합니다.
- **배포 간소화**: Docker 이미지를 통해 애플리케이션을 쉽게 배포할 수 있으며, 여러 환경(로컬, 스테이징, 프로덕션)에서 동일하게 실행할 수 있습니다.
- **자원 효율성**: Docker 컨테이너는 경량으로 작동하므로, VM(Virtual Machine)보다 자원을 더 효율적으로 사용할 수 있습니다.

**Docker와 Big Data의 연관성:**

- **데이터 처리 파이프라인**: Big Data 애플리케이션은 다양한 도구와 라이브러리를 필요로 합니다. Docker를 사용하면 이러한 도구들을 컨테이너화하여 복잡한 데이터 처리 파이프라인을 쉽게 구축하고 관리할 수 있습니다.
- **확장성 및 배포**: 분산 데이터 처리 시스템(예: Hadoop, Spark)을 Docker 컨테이너로 배포하면, 클러스터의 확장성과 관리를 간소화할 수 있습니다.
- **테스트 및 개발 환경**: Big Data 애플리케이션 개발 및 테스트 시, Docker를 사용하면 일관된 테스트 환경을 제공하여 개발 주기를 단축할 수 있습니다.

### Cloud Computing과 Big Data는 어떤 연관이 있나요?

**Cloud Computing과 Big Data의 연관성:**

- **확장성**: 클라우드 컴퓨팅은 사용자가 필요할 때 컴퓨팅 자원을 동적으로 확장하거나 축소할 수 있도록 지원합니다. 이는 대량의 데이터를 처리하는 Big Data 애플리케이션에 매우 유용합니다.
- **비용 효율성**: 클라우드 서비스는 사용한 만큼만 비용을 지불하는 방식(pay-as-you-go)을 제공하므로, 대규모 데이터 처리를 위해 고가의 하드웨어를 구매할 필요가 없습니다.
- **데이터 저장소 및 관리**: 클라우드 서비스는 대규모 데이터를 저장하고 관리할 수 있는 다양한 솔루션(예: Amazon S3, Google Cloud Storage)을 제공합니다. 이를 통해 Big Data를 쉽게 저장하고 액세스할 수 있습니다.
- **분산 데이터 처리**: 클라우드 플랫폼은 분산 데이터 처리 프레임워크(예: Amazon EMR, Google Dataproc)를 제공하여, 복잡한 데이터 처리 작업을 쉽게 수행할 수 있도록 지원합니다.

### JupyterLab은 Big Data 처리 관점에서 어떤 용도로 사용하면 좋을까요?

**JupyterLab의 Big Data 처리 용도:**

- **데이터 분석 및 시각화**: JupyterLab은 데이터 분석가와 과학자들이 인터랙티브하게 데이터를 분석하고 시각화할 수 있는 환경을 제공합니다. 파이썬, R 등 다양한 언어를 지원하며, 여러 데이터 시각화 라이브러리(예: Matplotlib, Seaborn, Plotly)와 통합됩니다.
- **프로토타이핑**: JupyterLab은 데이터를 빠르게 탐색하고 실험할 수 있는 유연한 환경을 제공하여, 데이터 처리 파이프라인의 프로토타이핑에 적합합니다.
- **교육 및 협업**: JupyterLab 노트북을 통해 데이터를 시각적으로 설명하고, 코드와 결과를 공유함으로써 교육 및 협업을 촉진할 수 있습니다.
- **분산 데이터 처리**: JupyterLab은 Apache Spark와 같은 분산 데이터 처리 프레임워크와 통합되어, 대규모 데이터를 처리하고 분석하는 데 사용할 수 있습니다.

### Distributed Computing과 Big Data는 어떤 연관이 있나요?

**Distributed Computing과 Big Data의 연관성:**

- **데이터 처리 속도 향상**: 분산 컴퓨팅은 여러 노드에 작업을 분배하여 병렬로 처리함으로써 대량의 데이터를 빠르게 처리할 수 있습니다. 이는 Big Data 애플리케이션에서 중요한 요소입니다.
- **확장성**: 분산 컴퓨팅은 데이터 양이 증가함에 따라 쉽게 노드를 추가하여 시스템을 확장할 수 있는 유연성을 제공합니다. 이는 Big Data 환경에서 필수적인 요구사항입니다.
- **신뢰성과 가용성**: 분산 컴퓨팅 시스템은 데이터 복제와 장애 조치를 통해 높은 신뢰성과 가용성을 제공합니다. 이는 대규모 데이터 처리에서 데이터 손실을 방지하고 시스템의 지속적인 운영을 보장하는 데 중요합니다.
- **비용 절감**: 분산 컴퓨팅은 여러 저비용 서버를 사용하여 고성능을 달성할 수 있으므로, 데이터 센터의 비용 효율성을 높일 수 있습니다.

이와 같이 Docker, 클라우드 컴퓨팅, JupyterLab, 분산 컴퓨팅은 모두 Big Data 처리에서 중요한 역할을 합니다. 각 기술은 데이터 처리, 분석, 저장 및 관리의 다양한 측면에서 Big Data 애플리케이션을 지원합니다.

[multiprocessing — 프로세스 기반 병렬 처리](https://docs.python.org/ko/3.11/library/multiprocessing.html#multiprocessing.Queue)

## M1. Multiprocessing : Pool

> multiprocessing 모듈은 파이썬에서 병렬 처리를 구현하기 위한 기능을 제공하는 모듈
이중 Pool 클래스의 경우 여러 프로세스를 풀에서 관리하고 작업을 수행할 수 있음.
> 

## M2. Multiprocessing : Process

> Process를 포크하여 작업을 수행하는 기능을 제공하는 모듈.
cpu bound 작업은 multi processing이 적합함
io bound 작업은 multi threading이 적합함
> 

## M3. Multiprocessing : Queue

> Queue는 multiprocessing 모듈의 클래스로서
멀티 프로세싱을 위한, 즉 자원은 공유하기 위한 큐 입니다.
프로세스는 각각 독립적인 프로세스 메모리 영역을 가지고 있습니다. 따라서 자원을 공유하지 않습니다.

프로세스간 자원 공유를 위해 커널에서 IPC를 제공합니다.

”파이프와 몇 개의 록/세마포어를 사용하여 구현된 프로세스 공유 큐를 반환합니다. 프로세스가 처음으로 항목을 큐에 넣으면 버퍼에서 파이프로 객체를 전송하는 피더 스레드가 시작됩니다.”
> 

## M4. Multiprocessing : all-in-one

> 이 연습 문제는 10개의 작업을 4개의 프로세스가 병렬적으로 수행하는 문제입니다.
부모 프로세스는 자식 프로세스들과 공유 가능한 Queue를 생성하여 정보를 공유합니다.
자식 프로세스는 공유된 큐에서 데이터를 병렬적으로 처리합니다.

multiprocessing 모듈의 Queue는 critical section에 대한 처리가 되어있습니다
queue에서 데이터를 꺼내는 작업은 FIFO 순서이지만, queue에서 데이터를 꺼낸 순서가
그 데이터를 처리하여 작업을 마친 순서임은 보장할 수 없습니다
> 

## M5. Sentiment Analysis - 팀 활동

```markdown
* 팀 활동 요구사항
제공된 데이터셋과 유사한 데이터셋을 웹 스크레이핑을 통해 만든 다음, word cloud를 만들어 봅시다.
데이터셋을 만들 때 어떤 작업들이 추가적으로 필요할까요?
prototyping에는 최소 1,000개 이상의 데이터를 사용하세요.
해당 분석을 통해 어떤 비즈니스 가치를 만들 수 있을지에 대해 토의합시다.
```

### 절차

<aside>
💡 1. 웹 스크래핑을 통한 데이터 추출 → CSV 형태로 저장 (Extract → Load)
2. CSV 파일을 읽어 전처리 하여 Word Cloud 생성 (Transform, Analyze)

</aside>

### 프로토타이핑

- 사용할 데이터 셋 : 네이버 웹툰 댓글
- 데이터셋을 만들 때 필요한 작업 : Sentiment 수준에 대한 정보를 함께 다뤄야 합니다.
    - 댓글의 공감/비공감 수치를 통해 감정 분석을 진행함 여러가지 방법이 있을 수 있음

```python
[방법1]
(공감 - 비공감) > 0 인 경우 긍정으로 분류
(공감 - 비공감) < 0 인 경우 부정으로 분류
이외에는 중립

[방법2]
(공감 - 비공감) > 0 인 경우 긍정으로 분류, |공감 - 비공감| 만큼 가중치
(공감 - 비공감) < 0 인 경우 부정으로 분류, |공감 - 비공감| 만큼 가중치
이외에는 중립
```

### 비즈니스 가치 (Business value)

```python
Word Cloud를 통해 감정 분석을 수행하여 다음과 같은 결과를 얻습니다.
긍정 단어, 부정 단어 중 빈도수가 높은 단어들을 시각적으로 확인할 수 있습니다.

이렇게 얻은 '단어'들을 통해 다음과 같은 가치를 창출할 수 있을 것으로 보입니다.
1. 브랜드 : 하나의 브랜드로서 사업을 확장할 때 참고할 수 있습니다.
	1) 브랜드 슬로건, 카피 제작에 활용
	2) 굿즈 제작게 활용(카드, 옷, 이모티콘)
	
2. 작품성
	1) 시각화된 단어 목록을 통해 웹툰의 정체성을 파악할 수 있습니다.
	2) 작가는 이를 참고하여 작업의 방향성을 결정할 수 있습니다.
```

- 결과 : 브랜드로서 사업을 확장할 만한, 작품성을 파악하고 발전시킬만한 데이터 및 데이터 분석 결과를 얻지 못하였습니다.

### 비즈니스 가치에 대한 근거

```python
# 근거 자료, refference (해당 분야 전문가의 글, 논문, 실제로 확인할 수 있는 내용 등) 찾기

1. 광고 카피의 가치
[레퍼런스]
유명한 광고 카피 예시 ~~
~ 에 따르면 광고 카피의 가치는 ~ 정도
-> 몇개의 단어로 이루어진 짧은 한 문장의 가치는 이렇게 높다는 점 강조
어떤 웹툰을 상징하는 짧은 슬로건, 카피 또한 높은 부가가치를 생산할 수 있는 요소이다.
이것들을 만드는데 도움이 된다

2. 실제 웹툰의 사업 확장 과정
최고심, 마루는 강아지, 등... 웹툰에서 사업 규모가 커진 웹툰들 예시
어떤 형태의 사업으로 확장이 되었는지 (아마 굿즈, 콜라보, 캐릭터 사업)

3. 카드, 옷, 이모티콘 등 디자인 요소에 '단어'가 들어가는 굿즈의 형태
카드, 옷, 이모티콘 등에 '단어' 들이 들어가있는 모습을 제시
사람들의 요구사항에는 즐거움이 있고 -> 이런 즐거움을 충족시켜주는 인기있는 단어들이 분명히 존재(밈?)
(like AK47?, 최고심 밈, 준비갈완료!!!!!)

4. 댓글을 통한 작가와 유저의 소통 사례
작가가 댓글을 통해 유저와 소통하는 사례를 -> 아마 후기에서 찾을 수 있을것임
작가가 기존 댓글 창을 통해 확인할 수 있는 것
* 평점
* 높은 공감의 댓글 (소수)

Problem (한계) -> 높은 공감의 댓글들이 전체를 반영하지 않을 수 있음 / 편향의 가능성도 존재함
Solve (해결) ->
크롤링 기반 감정 분석을 통해 낮은 공감을 가지고 있는 수많은 댓글들을 word cloud로 만들 수 있음.
만들어진 word cloud를 통해 한눈에(시간적인 비용을 들이지 않고) 댓글의 내용을 확인할 수 있음.
```

기대되는 결과들은 위와 같은 가치들을 지니는 데이터였습니다. 위와 같은 가치가 비즈니스적으로 어떤 효용이 있는지 근거를 들고자 하였습니다. 하지만 결과가 기대에 미치지 못하였기 때문에 근거를 들 필요가 없어졌습니다.

---

### 데이터 크롤링(E,L)

- selenium 사용
- 웹툰 댓글 데이터 처리를 위해 전체 댓글 보기 설정(클린 봇 해제, 추천 댓글→전체 댓글 전환)
- 댓글 ‘더 보기’ 버튼 클릭
    - 마지막 댓글까지 반복 수행
- 댓글들의 상위 컨테이너를 찾아 개별 댓글 DOM 객체들을 찾은 후 문장과 긍정/부정 공감을 추출
    - 삭제된 댓글의 구조가 달라 예외처리 진행하였습니다.
- DataFrame으로 변환한 후 csv파일로 저장
    - 'text', 'pos', 'neg', 'distance' : 문장, positive 공감 수, negative 공감수, pos - neg 값

### 데이터 전처리(T)

- pandas 라이브러리를 통해 csv 파일을 불러와 Transform 수행
- distance attribute에 대한 value가 양수인 문장과 음수인 문장을 positive_comments와 negative_comments로 분류
- 문장에서 단어들을 추출하기 위한 함수 구현
    
    ```python
    okt = Okt()
    
    # 한국어 불용어 리스트 (필요에 따라 직접 추가)
    stop_words = set(['의', '가', '이', '은', '들', '을', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다', '아', '서', '게' ,'다' ,'잔' ,'화' ,'외' ,'거'])
    
    def preprocess(text):
    		text = re.sub(r'\b[ㄱ-ㅎ]+\b', '', text)
        text = re.sub(r'[^\w\s]', '', text)  # 특수 문자 제거
        text = re.sub(r'\d+', '', text)  # 숫자 제거
        tokens = okt.morphs(text)
        tokens = [word for word in tokens if word not in stop_words]
        return tokens
    ```
    
    - 자음만 있는 문자 제거
    - 특수 문자 제거
    - 숫자 제거
    - okt 모듈을 통해 형태소 분할
    - 불용어 제거
- apply를 통한 병렬 처리
    
    ```python
    positive_tokens = positive_comments.apply(preprocess)
    negative_tokens = negative_comments.apply(preprocess)
    ```
    
    apply는 각 문장에 대한 처리를 병렬적으로 수행하도록 합니다.
    

### 워드 클라우드 생성

- sampling 방법 : 가장 빈번하게 나타난 상위 100개의 단어를 word cloud로서 시각화
- WordCloud 라이브러리 사용

[W2M5]

## 심화 학습

### Word Cloud

**word cloud의 작동 방법 - 어떤 로직으로 시각화가 이루어지는 - 을 개인 위키에 기술하세요.**

- 서론

```python
word cloud가 어떤 방식으로 단어들을 그려내는지 알아보고자한다.
wordcloud 모듈을 사용한 결과로 얻는 이미지의 특징을 바탕으로 어떻게 동작 하는지 예측해본다.
wordcloud github, docs를 확인하여 어떤 방식으로 동작하는지 확인한다.
wordcloud는 오픈소스로서 코드가 공개되어있다. 코드를 직접 확인하여 어떤 방식으로 동작하는지 확인한다.
```

- 이미지의 특징

```python
wordcloud 모듈을 사용한 결과
- 수많은 단어들에 대하여 '단어'를 '키', '갯수'를 '값'으로 하는 딕셔너리를 전달 받아 이미지를 생성
- max_words = 200 으로 최대 200개의 단어를 이미지에 나타내었다.
- 글씨 폰트, 너비, 높이, 배경 등 여러 속성을 추가할 수 있었다.
- 많이 등장한 단어는 크게, 조금 등장한 단어는 작게 그려졌다.
- 단어들의 방향이 가로, 세로 방향으로 나타난다.
- 단어들은 겹쳐지지 않으면서도 빈 공간에 오밀조밀하게 들어가있다.
- 색상이 다양하다...
- 기타 등등
```

- 예측

```python
- 단어의 빈도수에 대해 크기가 달리지지만 빈도수에 절대적이지는 않고 상대적일 것으로 예상된다.
- max_words 값을 바탕으로 그릴 단어들을 선택할 것이다.
- 폰트, 너비, 높이, 배경 등 여러 속성이 색상을 찍을 때 사용될 것이다.
- 단어를 그릴 때 가로, 세로를 랜덤으로 결정할 것이다.
- 단어들을 그리기 위한 영역을 선택하고 이미 선택된 영역에는 그릴 수 없도록 되어있을 것이다.
- 단어들을 그리기 위한 좌표 연산이 분명 있을것이다.
```

- worldcloud에서 그림을 그리는 방법
    - github, docs를 확인해본 결과 어떤 방식으로 wordcloud를 생성하는지 원리에 대해서는 설명되어있지 않다.
    - 단지 wordcloud를 통해 그림을 그리는 방법, 즉 모듈 사용 방법만 설명되어있다.
    - 따라서 코드를 분석해보았다.
    - worldcloud의 메소드, 필드들을 파악하여 어떻게 이미지를 완성하는지 확인하였다.
    - 본인은 Top down 방식으로 확인하였으나 설명은 Bottom up 방식으로 하는것이 이해가 쉬울듯 하다. (파일 → 이미지 → 연산과정 → 입력값)
    - 단어들을 그려낼 영역을 어떻게 선택하는지가 가장 핵심 알고리즘이라고 생각한다.
    - 마스킹을 통해 워드 클라우드의 모양을 선택할 수 있다. 이 기능을 포함한다.

---

```python
def to_file(self, filename):
        """Export to image file.

        Parameters
        ----------
        filename : string
            Location to write to.

        Returns
        -------
        self
        """

        img = self.to_image()
        img.save(filename, optimize=True)
        return self
        
```

to_file() 메소드는 WordCloud 클래스의 메소드이다. 현재 객체에서 to_image() 메소드를 통해 반환된 img의 save()메소드를 수행한다. 이 결과 이미지 파일이 저장된다.

img에 저장되는 객체는 PIL(The Python Imaging Library)의 Image 객체이다. 이미지는 픽셀에 rgb(a)값이 저장되어있는 구조이므로 이와 관련된 구조로 생각된다.

WorldCloud.to_image()의 반환값을 알기 위해 해당 메소드로 거슬러 올라가보자.

---

```python
def to_image(self):
        self._check_generated()
        if self.mask is not None:
            width = self.mask.shape[1]
            height = self.mask.shape[0]
        else:
            height, width = self.height, self.width

        img = Image.new(self.mode, (int(width * self.scale),
                                    int(height * self.scale)),
                        self.background_color)
        draw = ImageDraw.Draw(img)
        for (word, count), font_size, position, orientation, color in self.layout_:
            font = ImageFont.truetype(self.font_path,
                                      int(font_size * self.scale))
            transposed_font = ImageFont.TransposedFont(
                font, orientation=orientation)
            pos = (int(position[1] * self.scale),
                   int(position[0] * self.scale))
            draw.text(pos, word, fill=color, font=transposed_font)

        return self._draw_contour(img=img)
```

우선 to_image() 메소드는 WorldCloud 클래스의 메소드이다.

순차적으로 확인할 수 있는 내용은 다음과 같다.

self.mask 필드가 있는 경우와 없는 경우에 따라 width, height값이 바뀐다.

img 변수에 Image 객체를 생성한다. mode, scaling된 width, height, background_color를 인자로 하여 Image를 생성하다.

draw에는 ImageDraw 객체가 전달된다. ImageDraw 클래스는 PIL(The Python Imaging Library)에 속해있으며 이미지에 이미지를 그리는 역할을 한다. ImageDraw객체는 text()메소드를 가지고 있으며 이 메소드는 인자로 받은 위치에 폰트를 적용하여 text를 그려낸다.

self.layout_은 iterable한 자료구조로 보이며 item으로 [(word, count), font_size, position, orientation, color] 를 가지고 있는것으로 보인다. 이 값들과 WorldCloud의 필드 값들을 통해 text() 메소드의 파라미터를 구성한다.

self._draw_contour()은 to_mage()에서 그린 이미지에 mask 이미지의 테두리를 그리는 함수입니다. self.mask가 없거나 self.contour_width == 0 이면 to_mage()에서 그린 이미지를 그대로 반환하고, 그렇지 않으면 테두리를 img에 그린 후 img를 반환합니다.

단어, 폰트 사이즈, 위치, 방향, 색상 등이 저장되어있는 self.layout_이 어떻게 생성되는지가 중요하게 여겨집니다. 따라서 self.layout_을 초기화하는 코드를 확인해보겠습니다. self.layout_은 WordCloud 클래스의 generate_from_frequencies() 메소드에서 초기화됩니다. generate_from_frequencies() 메소드를 확인해봅시다.

---

```python
def generate_from_frequencies(self, frequencies, max_font_size=None):  # noqa: C901
        """Create a word_cloud from words and frequencies.

        Parameters
        ----------
        frequencies : dict from string to float
            A contains words and associated frequency.

        max_font_size : int
            Use this font-size instead of self.max_font_size

        Returns
        -------
        self

        """
        # make sure frequencies are sorted and normalized
        frequencies = sorted(frequencies.items(), key=itemgetter(1), reverse=True)
        if len(frequencies) <= 0:
            raise ValueError("We need at least 1 word to plot a word cloud, "
                             "got %d." % len(frequencies))
        frequencies = frequencies[:self.max_words]

        # largest entry will be 1
        max_frequency = float(frequencies[0][1])

        frequencies = [(word, freq / max_frequency)
                       for word, freq in frequencies]

        if self.random_state is not None:
            random_state = self.random_state
        else:
            random_state = Random()

        if self.mask is not None:
            boolean_mask = self._get_bolean_mask(self.mask)
            width = self.mask.shape[1]
            height = self.mask.shape[0]
        else:
            boolean_mask = None
            height, width = self.height, self.width
        occupancy = IntegralOccupancyMap(height, width, boolean_mask)

        # create image
        img_grey = Image.new("L", (width, height))
        draw = ImageDraw.Draw(img_grey)
        img_array = np.asarray(img_grey)
        font_sizes, positions, orientations, colors = [], [], [], []

        last_freq = 1.

        if max_font_size is None:
            # if not provided use default font_size
            max_font_size = self.max_font_size

        if max_font_size is None:
            # figure out a good font size by trying to draw with
            # just the first two words
            if len(frequencies) == 1:
                # we only have one word. We make it big!
                font_size = self.height
            else:
                self.generate_from_frequencies(dict(frequencies[:2]),
                                               max_font_size=self.height)
                # find font sizes
                sizes = [x[1] for x in self.layout_]
                try:
                    font_size = int(2 * sizes[0] * sizes[1]
                                    / (sizes[0] + sizes[1]))
                # quick fix for if self.layout_ contains less than 2 values
                # on very small images it can be empty
                except IndexError:
                    try:
                        font_size = sizes[0]
                    except IndexError:
                        raise ValueError(
                            "Couldn't find space to draw. Either the Canvas size"
                            " is too small or too much of the image is masked "
                            "out.")
        else:
            font_size = max_font_size

        # we set self.words_ here because we called generate_from_frequencies
        # above... hurray for good design?
        self.words_ = dict(frequencies)

        if self.repeat and len(frequencies) < self.max_words:
            # pad frequencies with repeating words.
            times_extend = int(np.ceil(self.max_words / len(frequencies))) - 1
            # get smallest frequency
            frequencies_org = list(frequencies)
            downweight = frequencies[-1][1]
            for i in range(times_extend):
                frequencies.extend([(word, freq * downweight ** (i + 1))
                                    for word, freq in frequencies_org])

        # start drawing grey image
        for word, freq in frequencies:
            if freq == 0:
                continue
            # select the font size
            rs = self.relative_scaling
            if rs != 0:
                font_size = int(round((rs * (freq / float(last_freq))
                                       + (1 - rs)) * font_size))
            if random_state.random() < self.prefer_horizontal:
                orientation = None
            else:
                orientation = Image.ROTATE_90
            tried_other_orientation = False
            while True:
                if font_size < self.min_font_size:
                    # font-size went too small
                    break
                # try to find a position
                font = ImageFont.truetype(self.font_path, font_size)
                # transpose font optionally
                transposed_font = ImageFont.TransposedFont(
                    font, orientation=orientation)
                # get size of resulting text
                box_size = draw.textbbox((0, 0), word, font=transposed_font, anchor="lt")
                # find possible places using integral image:
                result = occupancy.sample_position(box_size[3] + self.margin,
                                                   box_size[2] + self.margin,
                                                   random_state)
                if result is not None:
                    # Found a place
                    break
                # if we didn't find a place, make font smaller
                # but first try to rotate!
                if not tried_other_orientation and self.prefer_horizontal < 1:
                    orientation = (Image.ROTATE_90 if orientation is None else
                                   Image.ROTATE_90)
                    tried_other_orientation = True
                else:
                    font_size -= self.font_step
                    orientation = None

            if font_size < self.min_font_size:
                # we were unable to draw any more
                break

            x, y = np.array(result) + self.margin // 2
            # actually draw the text
            draw.text((y, x), word, fill="white", font=transposed_font)
            positions.append((x, y))
            orientations.append(orientation)
            font_sizes.append(font_size)
            colors.append(self.color_func(word, font_size=font_size,
                                          position=(x, y),
                                          orientation=orientation,
                                          random_state=random_state,
                                          font_path=self.font_path))
            # recompute integral image
            if self.mask is None:
                img_array = np.asarray(img_grey)
            else:
                img_array = np.asarray(img_grey) + boolean_mask
            # recompute bottom right
            # the order of the cumsum's is important for speed ?!
            occupancy.update(img_array, x, y)
            last_freq = freq

        self.layout_ = list(zip(frequencies, font_sizes, positions,
                                orientations, colors))
        return self
```

self.layout_ = list(zip(frequencies, font_sizes, positions, orientations, colors)) 이 코드를 보면 frequencis, font_sizes, positions,orientations, colors들을 zip한 후 list화 한 것을 알 수 있다.

- ~~행렬을 Transpose한 것과 비슷한 느낌?~~

아무튼 파라미터별로 같은 index의 값들을 하나의 배열로 합쳐논것이다. 그렇다면 frequencies, font_sizes, positions, orientations, colors가 어떤 자료들인지 확인하면 좋을 듯 하다.

이 함수를 위에서부터 순차적으로 확인해보자.

frequencies는 이전에 확인했듯이 <단어:빈도 = 키:값> 형태로 이루어진 딕셔너리이다. 빈도를 바탕으로 정렬한 후 max_wordsa만큼만 남긴다. 또한 빈도를 최대 빈도에 대한 상대 값으로 바꾸어 키,값을 쌍으로 하는 딕셔너리에서 키,값 튜플을 가지고 있는 리스트로 변환한다.

필드 값에 따라 필요한 필드에 대한 설정을 진해한다.

occupancy는 차지하는 면적에 관한 객체이다. 이후에 어떻게 사용되는지, 어떤 클래스인지 확인해야한다.

이후 grey img를 생성하는것으로 보아 공간에 대한 연산을 수행함을 알 수 있다.

이후 초기 필드 상태에 따라 font_size를 결정하는 코드를 볼 수 있다. max_font_size의 값에 따라  초기 font_size가 결정된다.

frequencies에서 빈도값을 바꾸는 작업을 하고 있다. 뭔가 단어들의 크기를 위한 것으로 추측된다.

이후 이전까지 작업한 것들을 바탕으로 단어들을 그레이 이미지로 그려 전체 영역에서 단어들이 들어갈 영역을 확인한다. 공간을 찾으면 font_sizes, positions, orientations, colors 각각의 리스트에 값을 추가한다. 이후 그레이 이미지를 통해 차지한 공간을 업데이트한다. 공간을 찾지 못하면 텍스트의 방향을 바꿔보고 폰트의 크기를 줄여나간다.

이렇게 만들어진 self.layout_을 통해 그려내게 되는 것이다.

그렇다면 단어가 겹치지 않게 배치하도록 공간 정보를 다루는 IntegralOccupancyMap의 객체 occupancy에 대해 알아보자.

---

```python
class IntegralOccupancyMap(object):
    def __init__(self, height, width, mask):
        self.height = height
        self.width = width
        if mask is not None:
            # the order of the cumsum's is important for speed ?!
            self.integral = np.cumsum(np.cumsum(255 * mask, axis=1),
                                      axis=0).astype(np.uint32)
        else:
            self.integral = np.zeros((height, width), dtype=np.uint32)

    def sample_position(self, size_x, size_y, random_state):
        return query_integral_image(self.integral, size_x, size_y,
                                    random_state)

    def update(self, img_array, pos_x, pos_y):
        partial_integral = np.cumsum(np.cumsum(img_array[pos_x:, pos_y:],
                                               axis=1), axis=0)
        # paste recomputed part into old image
        # if x or y is zero it is a bit annoying
        if pos_x > 0:
            if pos_y > 0:
                partial_integral += (self.integral[pos_x - 1, pos_y:]
                                     - self.integral[pos_x - 1, pos_y - 1])
            else:
                partial_integral += self.integral[pos_x - 1, pos_y:]
        if pos_y > 0:
            partial_integral += self.integral[pos_x:, pos_y - 1][:, np.newaxis]

        self.integral[pos_x:, pos_y:] = partial_integral
```

height, width, integral을 필드로 가지고 있다. mask의 유무에 따라 integral의 초기화가 달라진다. update() 메소드는 grey image를 image array의 형태로 변환하여 인자로 받아 integral을 업데이트한다. 그렇다면 integral은 어떤 역항르 하는지 알아보자.

sample_positioin() 메소드는 self.integral을 인자로 받는다. 이 메소드는 query_integral_image를 호출하여 이 함수의 반환값을 반환한다. query_integral_image는 어떤 함수인지 알아보자.

---

```python
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
import array
import numpy as np

def query_integral_image(unsigned int[:,:] integral_image, int size_x, int
                         size_y, random_state):
    cdef int x = integral_image.shape[0]
    cdef int y = integral_image.shape[1]
    cdef int area, i, j
    cdef int hits = 0

    # count how many possible locations
    for i in xrange(x - size_x):
        for j in xrange(y - size_y):
            area = integral_image[i, j] + integral_image[i + size_x, j + size_y]
            area -= integral_image[i + size_x, j] + integral_image[i, j + size_y]
            if not area:
                hits += 1
    if not hits:
        # no room left
        return None
    # pick a location at random
    cdef int goal = random_state.randint(0, hits)
    hits = 0
    for i in xrange(x - size_x):
        for j in xrange(y - size_y):
            area = integral_image[i, j] + integral_image[i + size_x, j + size_y]
            area -= integral_image[i + size_x, j] + integral_image[i, j + size_y]
            if not area:
                hits += 1
                if hits == goal:
                    return i, j
```

query_integral_image() 함수는 cython으로 구현되어있다. 파이썬 문법을 하고있지만 C언어로 변환된 이후에 컴파일하여 수행된다. query_integral_image.cpython-312-darwin.so 파일이 관련된 파일로 보인다. 아무튼 대충 함수 내용을 보면 입력받은 면적 만큼의 공간이 integral_image에 있는지 확인하는 함수이다. 누적합 알고리즘을 통해 최적화 되어있다. 약 픽셀 개수만큼에 대해 면적만큼 더 연산을 한다면 상당한 시간이 소요되지만 누적합 배열을 통해 기준 위치에 입력받은 면적만큼의 공간이 이용 가능 한지 아닌지 O(1)타임에 알 수 있다. 

### **추가학습거리**

[**Predicting Election Results from Twitter Using Machine Learning Algorithms**](https://www.researchgate.net/publication/343310126_Predicting_Election_Results_from_Twitter_Using_Machine_Learning_Algorithms)

**이 논문의 citation을 읽고 소감을 본인의 위키에 기술하세요.**

트위터 데이터를 감정 분석하여 선거 결과를 예측하는 방법(AI 모델)을 제안한 내용입니다. SVM을 사용하였고 상당히 높은 정밀도로 선거 결과를 예측하였다고 합니다. 트위터를 통해 선거 결과를 예측했다는 사실이 정말 놀랍고 흥미로웠습니다. 

최근 학습한 내용들과 관련하여 아래와 같은 궁금증이 생겼습니다.

1. 선거 결과를 예측하는 것은 어떤 경제적 가치를 창출하는가?
2. Unstructed 데이터인 트위터 데이터를 어떻게 수집하였을까?
3. 구체적으로 어떤 내용의 데이터를 수집하고 적재하였을까?
4. 인공지능 모델을 생성하고, 기계 학습을 수행하기 위해 데이터들을 어떤 방식으로, 어떤 형태의 데이터로 변환하였을까? (SVM 모델을 만들기 위해, 변환한 데이터들을 어떤 feature 로서 학습에 활용하였을까?) 

위와 같은 질문들을 던질 수 있고, 그 질문들에 대한 답을 찾아나갈 수 있는 사람이 되어야한다고 생각했습니다..!

[워드 클라우드 분석]

## M6. Cloud Computing?

<aside>
💡 학습 목표

1. **당신의 첫 Data Product (prototype) 배포하기**
2. **Local에서 docker container image를 만들어서 AWS EC2에 배포해 본다.자신이 만든 Data Product을 다른 사람이 사용할 수 있도록 배포한다.**
</aside>

- 기능 요구사항

**AWS EC2에 배포된 후에 서버 주소 (public DNS name)로 들어가면 JupyterLab 인터페이스가 실행되어야 합니다.해당 화면에서 W1에서 만들었던 Jupyter notebook을 선택해서 실행할 수 있어야 합니다.**

**W2에서 만든 노트북도 실행할 수 있도록 만드세요.**

- AWS 계정 만들기

> 계정 : aws.****@gmail.com
> 

- AWS free-tire EC2 생성하기 - 유저 데이터 사용

[EC2 인스턴스 생성]

- EC2 인스턴스 생성
    - AWS 회원가입 후 프리티어로 인스턴스를 생성합니다.
    
    리전 : us-east-1
    
    인스턴스 이름 : ****
    
    호스트 OS img : 
    
    > Amazon Linux 2023 AMI
    프리 티어 사용 가능
    ami-**** (64비트(x86), uefi-preferred) / ami-**** (64비트(Arm), uefi)
    가상화: hvm
    ENA 활성화됨: true
    루트 디바이스 유형: ebs
    > 
    
    CPU architect : amd/64 , x86
    
    키 페어 : ****
    
    storage : 30GiB, gp3
    
    - USER DATA를 활용하여 초기 인스턴스를 구성합니다.
    
    ```bash
    #!/bin/bash
    
    # Update the system
    sudo yum update -y
    
    # Install aws cli
    sudo yum install -y aws-cli
    
    # Install Docker
    sudo yum install docker -y
    
    # Start docker
    sudo service docker start
    
    # Add ec2-user to the docker group
    sudo usermod -aG docker ec2-user
    newgrp docker
    
    # Enable Docker service to start on boot
    sudo systemctl enable docker
    
    ```
    
    - 보안 관련 기타 설정사항
        - ssh, http 트래픽 허용
    
    <aside>
    💡 인스턴스 생성
    
    </aside>
    
    EC2 인스턴스에 연결하여 정상적으로 인스턴스가 부팅되었는지 확인합니다.
    
    - aws, docker이 user data에 의해 설치된채로 인스턴스가 구성되었습니다.
    
    ```bash
    [ec2-user@ip-172-31-19-254 ~]$ aws --version
    aws-cli/2.15.30 Python/3.9.16 Linux/6.1.96-102.177.amzn2023.x86_64 source/x86_64.amzn.2023 prompt/off
    
    [ec2-user@ip-172-31-19-254 ~]$ docker --version
    Docker version 25.0.3, build 4debf41
    ```
    
    - 탄력적 IP를 통해 public ip를 고정합니다

- Docker Image 생성하기

> **◦ 어떤 OS를 선택해야 할까요?
    ◦ 어떤 소프트웨어를 설치해야 할까요?
    ◦ 어떤 화일을 담아야 할까요?**
> 

[도커 이미지 빌드]

- 도커 이미지 빌드
    
    개발자의 컴퓨터에서 Docker를 통해 이미지를 빌드하고, Docker Desktop에서 이미지를 RUN하는 과정입니다.
    
    - Dockerfile
    
    ```python
    # 베이스 이미지로 Python 3.9 사용
    FROM python:3.9
    
    # 작업 디렉토리 설정
    WORKDIR /usr/src/****
    
    # 현재 디렉토리의 파일들을 컨테이너의 작업 디렉토리로 복사
    COPY . /usr/src/****
    
    # 필요한 패키지 설치
    RUN pip install --no-cache-dir jupyter
    
    # Jupyter Notebook이 실행될 포트 설정
    EXPOSE 8888
    
    # Jupyter Notebook 실행
    CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
    ```
    
    > 도커 파일 스크립트를 통해 이미지 빌드 설정을 할 수 있습니다.
    베이스 이미지를 사용하고, 작업 디렉토리를 설정하고
    도커 파일이 있는 디렉토리 상대 경로를 바탕으로 입력한 파일들을 컨테이너의 작업 디렉토리로 복사합니다.
    
    이 때 .dockerignore 파일을 사용하여 복사하지 않을 파일들을 설정할 수 있습니다.
    
    패키지를 설치할 때 requirements.txt 파일을 사용할 수 있습니다.
    
    수행될 프로세스에 대해 열어둘 포트를 설정하고, 프로그램을 실행 설정을 완료합니다.
    > 
    
    - 이미지 빌드
    
    ```bash
    # 형태
    docker build -t "image_name" .
    
    # 예시
    docker build -t **** .
    docker build --platform linux/amd64 -t **** .
    ```
    
    > build : 빌드 명령어
    -t **** : 태그 명령어
    . : 빌드 컨텍스트, . 은 현재 디렉토리를 빌드 컨텍스트로 사용하는것입니다.
    —platform : 컨테이너가 의존하는 os/cpu 아키텍처에 적합하게 빌드하는 옵션
    linux/amd64, linux/arm64 등이 있다…
    본인은 amd64로 진행하였다! 왜냐하면 aws linux/x86 이기 때문이다!!
    이미지를 빌드하는 컴퓨터가 맥북이라 amd64로 빌드하면 호환이 안된다!!
    > 
    
    - 이미지 RUN
    
    ```bash
    # 형태
    docker run -p 호스트포트:컨테이너포트 "image_name"
    
    # 예시
    docker run -p 8888:8888 ****
    ```
    
    호스트 포트에 대해 이 컨테이너(프로세스)가 listen을 하고, 컨테이너 내부 포트에 매핑합니다.
    
    > 우리는 도커 파일에서 EXPOSE 를 적었는데 왜 또 run 할때 저걸 적어줘야하나요…?
    이정도 고민을 할 수 있지만 저것은 이 컨테이너의 내부에 해당 숫자의 포트를 개방한다는 뜻이기 때문에 호스트 포트와 매핑하는 정보는 없습니다.
    > 
    
    [참조 공식문서]
    
    > EXPOSEThe EXPOSE instruction does not actually publish the port. It functions as a type of documentation between the person who builds the image and the person who runs the container, about which ports are intended to be published. To actually publish the port when running the container, use the -p flag on docker run to publish and map one or more ports, or the -P flag to publish all exposed ports and map them to high-order ports.
    > 
    
    EXPOSE 명령과 함께 작성하는 포트 번호는 실제로 노출하는 포트를 의미하지는 않지만, 이미지를 만드는 사람과 컨테이너를 실행시키는 사람 사이의 컨텍스트 공유를 위한 문서 역할정도로 보입니다. -https://junhyunny.github.io/information/docker/docker-file-expose-instruction/
    
    저도 위 말에 전적으로 동의합니다…!
    
    > 컨테이너는 프로세스입니다. 따라서 개방한 포트를 listen 합니다. 컨테이너는 가상머신은 아니지만 내부 네트워크 구조를 가지고 있습니다. 따라서 포트를 여러개 매핑할 수 있어야 할텐데.. 가능할까요? 네 가능합니다..! 아래와 같이 여러개의 명령행 인자를 넣을 수 있다고합니다.
    > 
    
    ```bash
    docker run -p 8888:8888 -p 9999:9999 my-jupyter-notebook
    ```
    
    로컬 호스트에서 접속이 이제 가능합니다.
    

- Docker Image 배포하기

[EC2에서 이미지 PULL (from ECR)]

- EC2에서 이미지 PULL
    - aws 웹 콘솔을 통해 연결
    
    > EC2 Instance Connect을 사용하여 연결
    퍼블릭 IPv4 주소가 있는 EC2 인스턴스 연결 브라우저 기반 클라이언트를 사용하여 연결합니다.
    > 
    
    aws 에서 제공하는 기능을 사용할 수 있습니다.
    
    - ssh 연결 방법
    
    > 인스턴스 ID : ****
    SSH 클라이언트를 엽니다.
    > 
    > 1. 프라이빗 키 파일을 찾습니다. 이 인스턴스를 시작하는 데 사용되는 키는 ****입니다.
    > 2. 필요한 경우 이 명령을 실행하여 키를 공개적으로 볼 수 없도록 합니다.
    > 
    > chmod 400 "****"
    > 
    > 1. 퍼블릭 DNS을(를) 사용하여 인스턴스에 연결:
    > 
    > ****.compute-1.amazonaws.com
    > 
    > 예:
    > 
    > ssh -i "****" ec2-user@****.compute-1.amazonaws.com
    > 
    
    저는 맥북에서 작업을 하기 때문에 zsh terminal을 사용하여 ssh 통신을 시도합니다.
    
    ****은 인스턴스 연결을 위해 만드는 key 이며 "****" 파일이 있는곳에서 ssh 연결을 시도하시면 됩니다. (아니면 경로를 포함하여 명령어를 작성하시면 됩니다.)
    
    외부 컴퓨터에서 인스턴스에 접근하기 위해서는 인바운드 설정이 되어있어야 합니다.
    
    > AWS에서 인바운드(inbound)과 아웃바운드(outbound) 규칙은 네트워크 트래픽의 허용 또는 차단을 관리하는 방법을 말합니다. 주로 Amazon EC2 인스턴스, VPC (가상 사설 클라우드), 서브넷 등의 네트워크 리소스에 적용됩니다. 각 규칙은 트래픽의 출발지와 목적지를 정의하고, 특정 프로토콜과 포트를 허용하거나 거부합니다.
    > 
    > 
    > ### 인바운드 규칙
    > 
    > **인바운드 규칙**은 외부에서 리소스로 들어오는 트래픽을 관리합니다. 주로 서버로의 접근을 허용하거나, 특정 서비스의 포트를 열어야 할 때 사용됩니다. 예를 들어, 웹 서버에 HTTP(포트 80)와 HTTPS(포트 443) 트래픽을 허용하는 인바운드 규칙을 설정할 수 있습니다.
    > 
    > ### 아웃바운드 규칙
    > 
    > **아웃바운드 규칙**은 리소스에서 외부로 나가는 트래픽을 관리합니다. 주로 인스턴스가 외부 서비스나 인터넷으로 연결되는 것을 제어할 때 사용됩니다. 예를 들어, 인스턴스가 인터넷으로 HTTP 요청을 보낼 수 있도록 아웃바운드 규칙을 설정할 수 있습니다. 
    > 
    
    위 내용은 Chat-gpt의 답변으로, 공식 문서를 참고하여 정확한 설명을 찾아보는것이 좋겠습니다.
    
    - 작업 컴퓨터에서와 마찬가지로 ec2 호스트에서 aws configure을 설정하고 도커 ecr 로그인을 진행합니다.
    
    도커 ecr 로그인
    
    > aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/****
    > 
    
    - 이미지 PULL 하기
    
    ```bash
    docker pull "URI"
    docker pull public.ecr.aws/****
    docker pull public.ecr.aws/****
    ```
    
    저는 퍼블릭 레포지토리를 사용하고있으며 이 레포지토리에 업로드 된 이미지의 URI는 “public.ecr.aws/****”입니다.
    
    이미지 URI는 aws ecr 페이지에서 확인 가능합니다.
    
    - 이미지 RUN 하기
    
    docker run -p 8888:8888 ****
    

<aside>
💡 팀 활동 요구사항

**Docker를 사용하는 이유가 뭘까요?
어떤 점은 더 불편한가요?
이번 미션에서는 하나의 EC2에 하나의 Docker container를 배포했습니다. 만약에 여러대의 EC2에 여러 개의 컨테이너를 배포해야 한다면 어떻게 해야 할까요?**

</aside>

- 도커를 사용하는 이유

> 어플리케이션의 인관된 실행 환경을 제공
빠른 테스트 및 배포가 가능함
가상 머신보다 가벼움
클라우드 컴퓨팅 기술과 함께 사용되기 좋음 → 배포, 운영의 자동화, 스케일링, 로드 밸런싱 등을 수월하게 할 수 있음
> 

- 불편한 점

> 어려움
일관된 실행 환경을 제공하긴 하지만, 그렇게 수행되는 어플리케이션을 구현하는 것은 오버헤드가 있음. 실제 개발환경과 동일하지 않을 수 있음
> 

- **여러대의 EC2에 여러 개의 컨테이너를 배포**

그냥 여러 인스턴스에 여러 컨테이너를 넣으면 된다..

여러 대의 인스턴스에 여러 컨테이너(어플리케이션)를 배포하여 운영 및 관리하기 위환 도구로 쿠버네티스가 있다. 이런 도구를 활용할 수 있다.

“쿠버네티스는 컨테이너화된 애플리케이션의 자동 디플로이, 스케일링 등을 제공하는 관리시스템으로, 오픈 소스 기반이다. 원래 구글에 의해 설계되었고 현재 리눅스 재단에 의해 관리되고 있다.”

## W2. 회고

이번 주도 정신 없이 지나갔습니다. 데이터 프로덕트란 무엇인지에 대해 배웠습니다. 시간이 없어서 할 수 없는 일이 아니라, 제한된 시간 내에서 우선순위가 높은 일과 높지 않아 하지 않을 일이 있어야 합니다. 시간을 계획적으로 잘 다루는것과 같은 말이라고 생각합니다. 어떤 문제를 해결할 수 있다고 하였을 때 사실 그것이 문제가 아니었을 수도 있다고 합니다. 연역적으로 검증되는게 아니라 귀납적으로 검증되는 것이 엔지니어링입니다. 따라서 의사 결정, 판단에 있어 근거에 너무 매몰될 필요는 없습니다. 그럼에도 불구하고 좋은 판단을 하는 노하우가 있을 것이라고 생각하여 프로젝트 과정에서 질문을 많이 남겨보고자 합니다.

멀티 프로세싱, 데이터 크롤링, 데이터 레이블링, 클라우드 서비스(EC2, ECR), Docker 등에 대해 학습하였습니다. 이런 도구들을 통해 어떤 Data Product를 생사할 수 있을지 고민해야합니다.

데이터 프로덕트를 만들 때 한번에 크게 만드는것보다, 문제상황, 필요한 대상 등을 좁히고 구체화여 시작해야합니다. 하나의 문제를 해결하고, 다른 문제들을 해결해 나가는 것이 데이터 프로덕트를 확장하는 과정입니다. 