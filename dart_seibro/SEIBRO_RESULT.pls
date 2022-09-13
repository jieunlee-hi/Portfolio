create or replace PROCEDURE SEIBRO_result
IS
BEGIN
DECLARE
--변수 선언
    ISSUE_INST_NAME SEIBRO.issue_inst_name%TYPE;
    ISIN_CODE SEIBRO.ISIN_CODE%TYPE;
    ISSUE_NAME_SEIBRO SEIBRO.ISSUE_NAME_SEIBRO%TYPE;
    GOODS_TYPE SEIBRO.GOODS_TYPE%TYPE;
    ISSUE_DATE SEIBRO.ISSUE_DATE%TYPE;
    EXPIRY_DATE SEIBRO.EXPIRY_DATE%TYPE;
    FUND_TYPE SEIBRO.FUND_TYPE%TYPE;
    ISSUE_CNT char(1000);
    CURSOR seibro_cur --커서정의
    IS
    SELECT ISIN_CODE
			 , GOODS_TYPE --파생결합증권 type 출력
			 , TRIM(REPLACE(ISSUE_NAME_SEIBRO,' ','')) ISSUE_NAME_SEIBRO --회차 여백 지우기
             ,ISSUE_INST_NAME --발행사 
             ,TO_NUMBER(REGEXP_REPLACE(REPLACE(ISSUE_NAME_SEIBRO,'100조',''), '[^0-9]', '')) ISSUE_CNT --발행회차만 추출
			 , ISSUE_DATE --발행일
          FROM SEIBRO  
         WHERE GOODS_TYPE IN ('ELS','DLS','DLB','ELB')  					-- ELS/DLS/DLB/ELB
           AND FUND_TYPE != '사모'							-- 사모 제외 (투자설명서는 공모만 존재)
           order by 4,5,6 desc
    ;

BEGIN
    OPEN seibro_cur;
    delete from seibro_tmp;
    LOOP --반복
        -- 커서에서 데이터 가져와서 하나씩 변수에 넣기
        FETCH seibro_cur INTO ISIN_CODE,GOODS_TYPE,ISSUE_NAME_SEIBRO,ISSUE_INST_NAME,ISSUE_CNT,ISSUE_DATE; 

            --DBMS_OUTPUT.ENABLE(NULL); --출력제한없음
            --출력문
            --DBMS_OUTPUT.PUT_LINE(ISIN_CODE||'  '||GOODS_TYPE||' '||ISSUE_INST_NAME||' '||ISSUE_CNT); 
            --다른테이블에 커서데이터insert
            insert into seibro_tmp values(ISIN_CODE,GOODS_TYPE,ISSUE_INST_NAME,ISSUE_CNT); 
            EXIT WHEN seibro_cur %NOTFOUND; --더이상 없을 경우 종료
    END LOOP;
    CLOSE seibro_cur; --커서 닫기
END;
end SEIBRO_result;


exec SEIBRO_result;