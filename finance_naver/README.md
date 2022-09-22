# 주요 증권사가 뽑은 2022 유망 업종 네이버 금융 종목 분석
####  관련기사 : https://hoyazzi.com/132

2022년 9월20일자 기준으로 2022유망업종 대표 3업종( 자동차 / 반도체와반도체장비 / 방송과엔터테인먼트 ) 종목들의 
네이버 금융사이트 속 주요금융지표 데이터들을 추출하여
크롤링, 전처리, 분석, 시각화를 다루는 프로젝트입니다.


> ## 주요 내용
* Pandas의 read_html, requests, BeautifulSoup 활용해 주가지표 데이터를 가져오는 함수를 작성하고 반복문 이용하여 여러 업종데이터 수집
* 데이터 목적에 맞게 자료구조형변환 ex) 리스트 -> 딕셔너리,  2차원리스트 -> 1차원리스트 , 리스트 -> 데이터프레임
* 결측치와 이상치 탐색 후 제거
* 정규표현식, astype, melt, merge, filter,append, concat, pivot,transpose 등의 기능을 활용하여 분석가능한 결과데이터생성
* to_csv , read_csv 이용하여 결과 파일 저장 및 읽어오기
* groupby, pivot_table, info, describe, value_counts 등을 통해 데이터 요약과 분석
* 다양한 시각화 방법 사용
   * 막대그래프(bar plot), 선그래프(line plot), 산점도/산포도(scatter plot,regplot,swarm plot), 상관관계(lm plot), 히트맵(Heatmap), 히스토그램(distplot), 파이차트(pie plot), 덴드로그램(dendrogram), 카테고리플롯(catplot), 박스플롯(boxplot), 패싯 그리드(factorplot) 등 

> ## 수집 데이터 출처
* 네이버 금융 업종별 : https://finance.naver.com/sise/sise_group.naver?type=upjong
    * 자동차 : https://finance.naver.com/sise/sise_group_detail.naver?type=upjong&no=278
    * 반도체와반도체장비 : https://finance.naver.com/sise/sise_group_detail.naver?type=upjong&no=273
    * 방송과엔터테인먼트 : https://finance.naver.com/sise/sise_group_detail.naver?type=upjong&no=285
* KRX 전체종목 :
    * FinanceDataReader 이용 
> ## 상세 내용
* [1_ 수집](https://github.com/jieunlee-hi/Portfolio/blob/main/finance_naver/1_%EC%88%98%EC%A7%91.ipynb) 
  * html 파일 수집하기 pd.read_html(url)
  * 결측 데이터 제거하기(axis 0:행, 1:열)
    * dropna(how="all")  : 모든 값이 전부 NaN인 행만 제거
    * dropna(subset=[''])  : 해당 컬럼값이 NaN인 행만 제거 
  * 데이터 프레임 합치기 pd.concat / pd.merge
  * 업종별 거래량 / 거래대금 시각화
    * seaborn /matplotlib
  * 파생변수 생성
    * datetime 이용하여 조회일자 컬럼생성
    * FinanceDataReader 사용하여 종목코드 컬럼생성
  * 주가 정보 수집 함수 생성
    * for문 사용하여 필요 데이터 수집
  * tqdm 사용 : 오래 걸리는 작업의 진행 상태 표시
  * 파일 저장 df.to_csv(file_name, index=False)
  * 파일 로드 pd.read_csv(file_name)
  
 * [2_ 전처리](https://github.com/jieunlee-hi/Portfolio/blob/main/finance_naver/2_%EC%A0%84%EC%B2%98%EB%A6%AC.ipynb)
    * 결측치 처리 : missingno이용 dendrogram 시각화 , dropna
    * 코스닥/코스피 :  한컬럼을 두컬럼으로 분류 (컬럼명에 '*' 있는 종목은 코스닥 종목) , pie차트 시가화
    * 시가총액, 시가총액 순위 : 정규표현식을 이용하여 필요글자만 추출
    * 동일업종PER : astype()사용하여 형변환
    * 배당 수익률/ PER|EPS / PBR|BPS : filter와 melt사용 tidydata생성, duplicated, unique사용하여 중복점검 

* [3_ 분석](https://github.com/jieunlee-hi/Portfolio/blob/main/finance_naver/3_%EB%B6%84%EC%84%9D.ipynb)
  * 결측치 처리: A_y값이 결측치일 경우 A_x값으로 대체
  * df["A"] = df["A_y"].fillna(df["A_x"])
  * 이상치 IQR값이용 이상치 제거
  * PER/PBR 상하위 최대/최소 종목 분석
    * sort_values / groupby 
    * max()/min()
    * 상관분석 corr()
    * 선형성 확인
  * 배당수익률이 높은종목
  * 코스피 중 시가총액이 가장 많은 종목
  * 코스피 중 거래량이 가장 많은 종목
  * 거래대금이 15위 안에 있는 코스피 종목의 "PER(배)" 분석
  * 컬럼 별 상관관계 분석
  * 시각화
    * seaborn 
      * catplot / barplot / boxplot / scatterplot / regplot / factorplot / heatmap  그래프사용
      * palette /color/ notch / edgecolor/ linewidth 등 그래프 옵션 사용 
    * matplotlib
      * hist() / bar() 사용
      * subplot / add_subplot / tight_layout() 등 사용
