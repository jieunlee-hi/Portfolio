create or replace PROCEDURE DARTS2SEIBRO
IS
BEGIN
DECLARE
    ISSUE_INST_NAME SEIBRO.issue_inst_name%TYPE;
    ISIN_CODE SEIBRO.ISIN_CODE%TYPE;
    ISSUE_NAME_SEIBRO SEIBRO.ISSUE_NAME_SEIBRO%TYPE;
    GOODS_TYPE SEIBRO.GOODS_TYPE%TYPE;
    ISSUE_DATE SEIBRO.ISSUE_DATE%TYPE;
    EXPIRY_DATE SEIBRO.EXPIRY_DATE%TYPE;
    FUND_TYPE SEIBRO.FUND_TYPE%TYPE;
    good_type SEIBRO.GOODS_TYPE%TYPE;
    issue_name DARTFSS.issue_name%TYPE;
    FSS_NO DARTFSS.FSS_NO%TYPE;
    goodtype SEIBRO.GOODS_TYPE%TYPE;
    issue_cnt SEIBRO_TMP.issue_cnt%TYPE;
    ISSUE_INST_NAME_1 SEIBRO_TMP.ISSUE_INST_NAME%TYPE;

    CURSOR join_cur --커서정의
    IS
    select * from
    (SELECT FSS_NO , ISSUE_INST_NAME, ISSUE_NAME ,
    CASE WHEN REPLACE(issue_name,' ','') LIKE '%주가연계증권%' OR
    REPLACE(issue_name,' ','') LIKE '%주가연계파생결합증권%'  OR
    REPLACE(issue_name,' ','') LIKE '%ELS%' THEN 'ELS'
    WHEN REPLACE(issue_name,' ','') LIKE '%파생결합증권%' OR 
    REPLACE(issue_name,' ','') LIKE '%기타파생결합증권%' THEN 'DLS'
    WHEN REPLACE(issue_name,' ','') LIKE '%주가연계파생결합사채%'OR
    REPLACE(issue_name,' ','') LIKE '%ELB%' THEN 'ELB'
    WHEN REPLACE(issue_name,' ','') LIKE '%기타파생결합사채%' OR 
    REPLACE(issue_name,' ','') LIKE '%파생결합사채%' OR
    REPLACE(issue_name,' ','') LIKE '%DLB%' THEN 'DLB'	
    ELSE 'N/A' END AS goodtype
    FROM DARTFSS)a 
    join SEIBRO_TMP on  a.issue_name LIKE '%'||trim(SEIBRO_TMP.issue_cnt)||'%'
    where  a.issue_inst_name =SEIBRO_TMP.issue_inst_name
    and SEIBRO_TMP.good_type = a.goodtype;


BEGIN
    OPEN join_cur;
    
    LOOP --반복
        FETCH join_cur INTO FSS_NO,issue_inst_name,issue_name,goodtype,ISIN_CODE,good_type,issue_inst_name_1,issue_cnt; --커서에서 데이터 가져와서 하나씩 변수에 넣기
        EXIT WHEN join_cur %NOTFOUND; --더이상 없을 경우 종료
            --DBMS_OUTPUT.ENABLE(NULL); 
            --DBMS_OUTPUT.PUT_LINE(FSS_NO||'  '||ISIN_CODE||' '||issue_inst_name||' '||issue_cnt||' '||goodtype); --출력문
            --다른테이블에 커서데이터insert
            insert into matching_result values(FSS_NO,ISIN_CODE,ISSUE_INST_NAME,ISSUE_CNT); 
    END LOOP;
    CLOSE join_cur; --커서 닫기
END;
end DARTS2SEIBRO;