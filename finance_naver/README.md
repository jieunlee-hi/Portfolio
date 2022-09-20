# 네이버 금융 업종별 종목 분석
네이버 금융에 나와있는 주가지표들을 가지고 
2022년 9월19일자 기준으로 네이버금융 업종별 종목들의 주요요소들을 추출하여
데이터를 판다스로 크롤링, 전처리, 분석, 시각화를 다루고 있습니다.
데이터를 Pandas의 melt, concat, pivot, transpose 와 같은 reshape 기능을 활용해 분석해 봅니다. 그리고 groupby, pivot_table, info, describe, value_counts 등을 통한 데이터 요약과 분석을 해봅니다. 
이를 통해 전혀 다른 형태의 두 데이터를 가져와 정제하고 병합하는 과정을 다루는 방법을 알게 됩니다. 전처리 한 결과에 대해 수치형, 범주형 데이터의 차이를 이해하고 다양한 그래프로 시각화를 할 수 있게 됩니다.


## 다루는 내용
* 네이버금융데이터를 활용해 주가지표 데이터를 가져와서 전처리 하기
* 판다스를 통해 데이터를 요약하고 분석하기
* 데이터 전처리와 병합하기
* 데이터의 형식에 따른 다양한 시각화 방법 이해하기
* 막대그래프(bar plot), 선그래프(line plot), 산포도(scatter plot), 상관관계(lm plot), 히트맵, 상자수염그림, swarm plot, 도수분포표, 히스토그램(distplot) 실습하기


## 데이터셋
* 수집 출처 : 
    * 네이버 금융 업종별 시세 : https://finance.naver.com/sise/sise_group.naver?type=upjong


네이버 금융 개별종목 수집
FinanceDataReader를 통해 수집했던 데이터를 네이버 증권 웹 페이지를 통해 직접 수집합니다.
Keyword
https://github.com/corazzon/finance-data-analysis/blob/main/3.3%20%EB%84%A4%EC%9D%B4%EB%B2%84%EA%B8%88%EC%9C%B5%20%EA%B0%9C%EB%B3%84%EC%A2%85%EB%AA%A9%20%EC%88%98%EC%A7%91-input.ipynb

## 사용 스킬 소개
* Pandas read_html로 데이터수집 하기
* Pandas로 데이터 로드해서 분석하기

Pandas : 파이썬의 대표적인 데이터 분석 도구
Numpy : 파이썬의 수치계산 도구
matplotlib : 파이썬의 대표적인 데이터 시각화 도구
seaborn : matplotlib 을 사용하기 쉽게 추상화 해 놓은 고수준 시각화 도구로 기본 통계 연산을 제공
plotly : 고수준, 저수준 시각화 기능을 제공하며 인터랙티브한 시각화 가능
Requests : 웹 페이지의 소스코드를 HTTP 통신으로 받아올 수 있는 도구 입니다.
BeautifulSoup4 : 웹 페이지의 소스코드에서 원하는 정보를 가져올 수 있는 도구 입니다.
