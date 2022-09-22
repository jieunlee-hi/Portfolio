# DART & SEIBRO 데이터 매칭 프로젝트
![제목 없음ff](https://user-images.githubusercontent.com/34561364/191533968-148c01c8-1dd3-451b-99d9-4844153cc54a.png)

## 비정형데이터와 정형데이터의 매칭
+ Main Goal
  + 파생결합증권 투자자들의 편의성 향상을 위하여 종목코드와 투자설명서 매칭
+ Overview
  + 투자설명서의 텍스트(비정형데이터) 추출을 위해 DART에서 제공하는 OPENAPI를 이용
  PYTHON으로 원하는 조건의 전자공시를  XML형식의 파일(반정형데이터)로 다운받아 전처리과정을 통해 원하는 형태의 값으로 데이터를 수집하여 
  PL/SQL을 이용하여 SEIBRO에서 제공하는 EXCEL 파일 (정형데이터) 속 종목코드와 해당되는 투자설명서 매칭
  
## 사용기술 및 관련 코드
### 데이터 수집 : PYTHON , EXCEL
#### [DART](https://github.com/jieunlee-hi/Portfolio/blob/main/dart_seibro/DART_Crawling.py)
* PYTHON - requests
* OPENAPI를 활용해 공시파일 다운로드 
  * 공시검색 API, 공시서류원본파일다운로드 API 사용 (참고 : https://opendart.fss.or.kr/guide/main.do?apiGrpCd=DS001)
  * zipfile 이용하여 xmlfile로 다운 
  * 텍스트 데이터 정제하여 원하는 텍스트 추출 - 정규 표현식  
#### [SEIBRO](https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/derivCombi/BIP_CNTS07015V.xml&menuNo=199)
  * seibro사이트 : 파생결합증권 ELS/ELB, DLS/DLB 데이터 엑셀 다운로드 
    
### 전처리 : Oracle Procedure
#### [SEIBRO_RESULT.pls](https://github.com/jieunlee-hi/Portfolio/blob/main/dart_seibro/SEIBRO_RESULT.pls)
* SEIBRO데이터 전처리 
  * ISSUE_CNT 컬럼생성
    * 종목명 (ISSUE_NAME_SEIBRO) 에서 회차를 나타내는 숫자[0-9] 만 뽑아내어 회차(ISSUE_CNT) 컬럼 생성
        * EX ) KB증권100조 1023회  => 1023
    * 증권구분 =  ELS / DLS / DLB / ELB 
    * 발행구분 = 공모 (사모 제외 : 투자설명서는 공모만 발행됨)
* 전처리 완료 후 필요 컬럼 seibro_tmp 테이블에 insert 
  * ISIN_CODE 종목코드, GOODS_TYPE 증권구분 , ISSUE_INST_NAME 발행기관명, ISSUE_CNT 발행회차
  
#### [DARTS2SEIBRO.pls](https://github.com/jieunlee-hi/Portfolio/blob/main/dart_seibro/DARTS2SEIBRO.pls)
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

### 데이터 매칭 : PL/SQL 
#### [select.sql](https://github.com/jieunlee-hi/Portfolio/blob/main/dart_seibro/select.sql)
* ACCEPT 사용 
  * 투자설명서를 원하는 종목코드를 입력하세요.
    * 입력받은 종목코드와 매치되는 투자설명서 주소 출력
    * 매치되는 데이터가 없을 시 : 존재하지않는코드:::
  


