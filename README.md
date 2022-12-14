# Data Analytics Portfolio
![아이콘](https://cdn.iconscout.com/icon/premium/png-256-thumb/data-analysis-1565652-1327717.png)

 # Project 1 - [2022 유망업종 금융데이터 분석](https://github.com/jieunlee-hi/Portfolio/tree/main/finance_naver)
 ------------
 ## 수집
 * Pandas의 read_html, requests, BeautifulSoup 활용해 주가지표 데이터를 가져오는 함수를 작성하고 반복문 이용하여 여러 업종데이터 수집
 * FinanceDataReader 이용하여 KRX 데이터 수집
 * [바로가기](https://github.com/jieunlee-hi/Portfolio/blob/main/finance_naver/1_%EC%88%98%EC%A7%91.ipynb)
 ## 전처리
 * 데이터 목적에 맞게 자료구조형변환 ex) 리스트 -> 딕셔너리,  2차원리스트 -> 1차원리스트 , 리스트 -> 데이터프레임
 * 결측치와 이상치 탐색 후 제거 ex) dropna, outlier 
 * 정규표현식, astype, melt, merge, filter,append, concat, pivot,transpose 등의 기능을 활용하여 분석가능한 결과데이터생성
 * to_csv , read_csv 이용하여 결과 파일 저장 및 읽어오기
 * [바로가기](https://github.com/jieunlee-hi/Portfolio/blob/main/finance_naver/2_%EC%A0%84%EC%B2%98%EB%A6%AC.ipynb)
## 분석
   * groupby, pivot_table, info, describe, value_counts, sort_values 등을 통해 데이터 요약과 분석
   * 상관분석 corr(), heatmap, 선형성 확인
   * 다양한 시각화 방법 사용
     * seaborn
       * catplot / barplot / boxplot / scatterplot / regplot / factorplot / heatmap 그래프사용
       * palette /color/ notch / edgecolor/ linewidth 등 그래프 옵션 사용
     * matplotlib
       * hist() / bar() 사용
       * subplot / add_subplot / tight_layout() 등 사용
  * [바로가기](https://github.com/jieunlee-hi/Portfolio/blob/main/finance_naver/3_%EB%B6%84%EC%84%9D.ipynb)
 # Project 2 - [DART비정형데이터와 SEIBRO 정형EXCEL데이터 매칭](https://github.com/jieunlee-hi/Portfolio/tree/main/dart_seibro)
 ------------
![gggg](https://user-images.githubusercontent.com/34561364/192132865-f43f4094-1620-4343-a22d-6e62d8abe24e.png)

### Main Goal
  + 파생결합증권 투자자들의 편의성 향상을 위하여 종목코드와 투자설명서 매칭
### Overview
  + 투자설명서의 텍스트(비정형데이터) 추출을 위해 DART에서 제공하는 OPENAPI를 이용
  PYTHON으로 원하는 조건의 전자공시를  XML형식의 파일(반정형데이터)로 다운받아 전처리과정을 통해 원하는 형태의 값으로 데이터를 수집하여 
  PL/SQL을 이용하여 SEIBRO에서 제공하는 EXCEL 파일 (정형데이터) 속 종목코드와 해당되는 투자설명서 매칭
  
### 사용기술 및 관련 코드

### 1. 데이터 수집 : PYTHON , EXCEL
#### 1-1. [DART](https://github.com/jieunlee-hi/Portfolio/blob/main/dart_seibro/DART_Crawling.py)
* PYTHON - requests
* OPENAPI를 활용해 공시파일 다운로드 
  * 공시검색 API, 공시서류원본파일다운로드 API 사용 (참고 : https://opendart.fss.or.kr/guide/main.do?apiGrpCd=DS001)
  * zipfile 이용하여 xmlfile로 다운 
  * 텍스트 데이터 정제하여 원하는 텍스트 추출 - 정규 표현식  
#### 1-2. [SEIBRO](https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/derivCombi/BIP_CNTS07015V.xml&menuNo=199)
  * seibro사이트 : 파생결합증권 ELS/ELB, DLS/DLB 데이터 엑셀 다운로드 
    
### 2. 전처리 : Oracle Procedure
#### 2-1. [SEIBRO_RESULT.pls](https://github.com/jieunlee-hi/Portfolio/blob/main/dart_seibro/SEIBRO_RESULT.pls)
* SEIBRO데이터 전처리 
  * ISSUE_CNT 컬럼생성
    * 종목명 (ISSUE_NAME_SEIBRO) 에서 회차를 나타내는 숫자[0-9] 만 뽑아내어 회차(ISSUE_CNT) 컬럼 생성
        * EX ) KB증권100조 1023회  => 1023
    * 증권구분 =  ELS / DLS / DLB / ELB 
    * 발행구분 = 공모 (사모 제외 : 투자설명서는 공모만 발행됨)
* 전처리 완료 후 필요 컬럼 seibro_tmp 테이블에 insert 
  * ISIN_CODE 종목코드, GOODS_TYPE 증권구분 , ISSUE_INST_NAME 발행기관명, ISSUE_CNT 발행회차
  
#### 2-2. [DARTS2SEIBRO.pls](https://github.com/jieunlee-hi/Portfolio/blob/main/dart_seibro/DARTS2SEIBRO.pls)
* DART 수집데이터의 종목명 이용하여 GOODTYPE(증권구분)컬럼생성 : 서브쿼리사용
   * ELS -> %주가연계증권%,%주가연계파생결합증권%,%ELS%
   * DLS -> %파생결합증권%,%기타파생결합증권%,%DLS%
   * ELB -> %주가연계파생결합사채% , %ELB%
   * DLB -> %파생결합사채%, %기타파생결합사채%, %DLB%
* seibro 전처리 데이터가 담긴 seibro_tmp 테이블과 JOIN하여 데이터매치
   * JOIN 조건 
     1. DART데이터 종목명에 SEIBRO의 발행회차가 포함되어있는 데이터
     2. DART와 SEIBRO 데이터의 발행회사가 동일
     3. DART와 SEIBRO 데이터의 증권구분 동일 (ex. ELS/DLS/ELB/DLB ) 
* 매칭 결과 MATCHING_RESULT 테이블에 insert

### 3. 데이터 매칭 : PL/SQL 
#### 3-1. [select.sql](https://github.com/jieunlee-hi/Portfolio/blob/main/dart_seibro/select.sql)
* ACCEPT 사용 
  * 투자설명서를 원하는 종목코드를 입력하세요.
    * 입력받은 종목코드와 매치되는 투자설명서 주소 출력
    * 매치되는 데이터가 없을 시 : 존재하지않는코드:::
  

 # Project 3- [환경 뉴스 텍스트마이닝](https://github.com/jieunlee-hi/Portfolio/tree/main/environment_news)
 ------------
![news (3)](https://user-images.githubusercontent.com/34561364/192138427-c2273446-eed5-42a7-9cc3-20df2bbbebf0.png)
## [상세설명 PDF 바로가기]()
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


