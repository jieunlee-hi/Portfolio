# 환경 뉴스 텍스트 마이닝
----------
![news (3)](https://user-images.githubusercontent.com/34561364/192138427-c2273446-eed5-42a7-9cc3-20df2bbbebf0.png)

## 텍스트 마이닝 (Text Mining) 이란?
> 비/반정형 텍스트 데이터에서 자연어처리(Natural Language Processing)기술에 기반하여 유용한 정보를 추출, 가공하는 것을 목적으로 하는 기술이다
  즉, 문서 중에 특정 단어가 얼마나 많이 출현하는지 단어 빈도(Term Frequency)를 찾아낸다. 이때 분석에 사용한 데이터는 뉴스인데 문장, 즉 자연어로 되어 있어서 문장 그대로 분석할 수 없다. 하나의 단어로 분리해야 하는데, 이를 형태소 분석이라고 한다.

# 텍스트 마이닝의 3단계 
## 1. 문서 수집 (Crawling)
##### 1) 자료 입수처 : 네이버 뉴스 > 사회 >  환경
(https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=102&sid2=252)
##### 2) 수집 데이터 내용 :
  pd.date_range로 지정한 1년간의 환경 뉴스 헤드라인 추출
     * 데이터 기간 : 2021.08.01  ~ 2022.07.31  
##### 3) 수집 기술 : PYTHON
    * html Parsing
    * BeautifulSoup 패키지

## 2. 형태소 분석 (NLP) (Konlpy)
* 문서(document) > 문단(paragraph) > 문장(sentence) > 어절 > 형태소 > 음절
* 형태소 : 의미를 가진 가장 작은 말의 단위. 더 나누면 뜻을 잃어버림.
##### 2-1) 빈도분석 (Counter 함수)
* okt 객체를 생성
* nouns 함수를 사용해 명사추출
* Counter에 넘겨준뒤 빈도수 구하기
##### 2-2) 연관규칙분석(apriori) _지지도, 신뢰도, 향상도
* 항목들 간의 관계를 얻기 위해 한 항목의 존재가 다른 항목의 존재를 암시하는 조합을 발견하는 분석방법
* 지지도는 X->Y = Y->X (상호대칭)
* 신뢰도는 X->Y ≠ Y->X (지지도가 낮아도 신뢰도가 높은 경우 유용한 규칙)
* 향상도는 X->Y = Y->X (상호대칭)
  * L > 1 : 양의 상관관계 (같이 구매할 확률 높음)
  * L < 1 : 음의 상관관계 (같이 구매할 확률 낮음)
  * L = 1 : 독립적 상관관계 (서로 영향 미치지 않음)
      
## 3. 시각화 (Word Cloud)
##### 3-1) seaborn - barplot , lmplot을 이용한 시각화
##### 3-2) Word Cloud 단어빈도 시각화 
  * 가장빈도가 큰 단어와 빈도가 가장 작은 단어 폰트 사이의 크기 차이를 주어 시각화
  * 연간 / 봄 / 여름 / 가을 / 겨울 
![제목 없음gggg](https://user-images.githubusercontent.com/34561364/192140267-735ce0ec-8beb-4a48-9d7b-372f08e14892.png)

