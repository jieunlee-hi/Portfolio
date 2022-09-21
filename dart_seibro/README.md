# DART & SEIBRO 데이터 매칭 프로젝트
![제목 없음ff](https://user-images.githubusercontent.com/34561364/191533968-148c01c8-1dd3-451b-99d9-4844153cc54a.png)

## 비정형데이터와 정형데이터의 매칭
+ Main Goal
  + 파생결합증권 투자자들의 편의성 향상을 위하여 종목코드와 투자설명서 매칭
+ Overview
  + 투자설명서의 텍스트(비정형데이터) 추출을 위해 DART에서 제공하는 OPENAPI를 이용
  원하는 조건의 전자공시를  XML형식의 파일(반정형데이터)로 다운받아 전처리과정을 통해 원하는 형태의 값으로 데이터를 수집하여 
  SEIBRO에서 제공하는 EXCEL 파일 (정형데이터) 속 종목코드와 해당되는 투자설명서 매칭
  
+ 사용기술 및 관련 코드
  + 데이터 수집 : PYTHON / OPENAPI /requests / EXCEL
    + dart_crawling.py
  * OPENAPI를 활용해 공시파일 다운로드 
  * 텍스트 데이터 정제하기 -  
  * 텍스트 데이터에서 원하는 정보 추출하기 
  * 문자열에서 원하는 텍스트 추출하기
  + 전처리 : PYTHON / Oracle Procedure
    + SEIBRO_RESULT.pls
    + DARTS2SEIBRO.pls
  + 데이터 매칭 : PL/SQL 
    + select.sql
    
  


