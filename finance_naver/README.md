# 주요 증권사가 뽑은 2022 유망 업종 네이버 금융 종목 분석
####  관련기사 : https://pbes.tistory.com/entry/%EC%A3%BC%EC%9A%94-%EC%A6%9D%EA%B6%8C%EC%82%AC%EA%B0%80-%EB%BD%91%EC%9D%80-2022%EB%85%84-%EC%9C%A0%EB%A7%9D-%EC%97%85%EC%A2%85-%EB%B0%8F-%EC%A2%85%EB%AA%A9%20import%20time

2022년 9월20일자 기준으로 2022유망업종 대표 3업종( 자동차 / 반도체와반도체장비 / 방송과엔터테인먼트 ) 종목들의 
네이버 금융사이트 속 주요금융지표 데이터들을 추출하여
크롤링, 전처리, 분석, 시각화를 다루는 프로젝트입니다.


> ## 주요 내용
* Pandas의 read_html, requests, BeautifulSoup 활용해 주가지표 데이터를 가져오는 함수를 작성하고 반복문 이용하여 여러 업종데이터 수집
* 데이터 목적에 맞게 형변환 ex) 리스트 -> 딕셔너리,  2차원리스트 -> 1차원리스트 , 리스트 -> 데이터프레임
* 판다스를 통해 수집한 로우데이터를 요약하고 분석하기
* 결측치와 이상치 탐색 후 제거
* 정규표현식, astype, melt, merge, filter,append, concat, pivot,transpose 등의 기능을 활용하여 분석가능한 결과데이터생성
* to_csv , read_csv 이용하여 결과 파일 저장 및 읽어오기
* groupby, pivot_table, info, describe, value_counts 등을 통해 데이터 요약과 분석
* 다양한 시각화 방법 사용
   * 막대그래프(bar plot), 선그래프(line plot), 산점도/산포도(scatter plot,regplot,swarm plot), 상관관계(lm plot), 히트맵(Heatmap), , 히스토그램(distplot) 파이차트(pie plot),덴드로그램(dendrogram),카테고리플롯(catplot),박스플롯(boxplot),패싯 그리드(factorplot) 등 

> ## 데이터출처
* 네이버 금융 업종별 : https://finance.naver.com/sise/sise_group.naver?type=upjong
    * 자동차 : https://finance.naver.com/sise/sise_group_detail.naver?type=upjong&no=278
    * 반도체와반도체장비 : https://finance.naver.com/sise/sise_group_detail.naver?type=upjong&no=273
    * 방송과엔터테인먼트 : https://finance.naver.com/sise/sise_group_detail.naver?type=upjong&no=285
* KRX 전체종목 :
    * FinanceDataReader 이용 
