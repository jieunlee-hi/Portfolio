# 네이버 금융 업종별 종목 분석
네이버 금융에 나와있는 주가지표들을 가지고 
2022년 9월20일자 기준으로 2022유망업종 대표 3업종( 자동차 / 반도체와반도체장비 / 방송과엔터테인먼트 ) 종목들의 주요금융지표데이터들을 추출하여
크롤링, 전처리, 분석, 시각화를 다루는 프로젝트입니다..

데이터를 Pandas의 melt, concat, pivot, transpose 와 같은 reshape 기능을 활용해 전처리하고
groupby, pivot_table, info, describe, value_counts 등을 통해 데이터 요약과 분석을 해봅니다.

이를 통해 전혀 다른 형태의 두 데이터를 가져와 정제하고 병합하는 과정을 다루는 방법을 알게 됩니다. 
전처리 한 결과에 대해 수치형, 범주형 데이터의 차이를 이해하고 다양한 그래프로 시각화를 할 수 있습니다.


* 네이버금융데이터를 활용해 주가지표 데이터를 가져와서 전처리 하기
* 판다스를 통해 로우데이터를 요약하고 분석하기
* 데이터 전처리와 병합하여 분석가능한 결과데이터생성
* 다양한 시각화 방법
* 막대그래프(bar plot), 선그래프(line plot), 산포도(scatter plot), 상관관계(lm plot), 히트맵, 상자수염그림, swarm plot, 히스토그램(distplot) pie plot
msno.dendrogram

## 데이터출처
* 네이버 금융 : 
    * 네이버 금융 업종별 시세 : https://finance.naver.com/sise/sise_group.naver?type=upjong
    * 자동차 : https://finance.naver.com/sise/sise_group_detail.naver?type=upjong&no=278
    * 반도체와반도체장비 : https://finance.naver.com/sise/sise_group_detail.naver?type=upjong&no=273
    * 방송과엔터테인먼트 : https://finance.naver.com/sise/sise_group_detail.naver?type=upjong&no=285
* KRX 전체종목 :
    * FinanceDataReader 이용 

## 사용 스킬
* Pandas read_html로 데이터 수집
* 결측 데이터 제거  : dropna
* 데이터 프레임 합치기 : concat, merge
* df.iloc
* datetime 이용하여 오늘일자 불러오기
* tqdm 사용 : 오래 걸리는 작업의 진행상태 표시
* to_csv 파일저장
* read_csv 파일읽기
* 정규표현식
* astype() 형변환
* filter / melt 
* rename 컬럼명 변경
