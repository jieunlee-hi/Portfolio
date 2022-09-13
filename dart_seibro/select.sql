SET VERIFY OFF
set serveroutput on;

ACCEPT P_ISIN_CODE PROMPT '투자설명서를 원하는 종목코드를 입력하세요. : ';
DECLARE
V_ISIN_CODE MATCHING_RESULT.ISIN_CODE%TYPE;
V_FSS_NO MATCHING_RESULT.FSS_NO%TYPE;
V_ISSUE_INST_NAME MATCHING_RESULT.ISSUE_INST_NAME%TYPE;
V_ISSUE_CNT MATCHING_RESULT.ISSUE_CNT%TYPE;
&P_ISIN_CODE  MATCHING_RESULT.ISIN_CODE%TYPE;
BEGIN
SELECT FSS_NO, trim(ISIN_CODE), ISSUE_INST_NAME, ISSUE_CNT
INTO   V_FSS_NO, V_ISIN_CODE,V_ISSUE_INST_NAME,V_ISSUE_CNT
FROM MATCHING_RESULT
WHERE ISIN_CODE = '&P_ISIN_CODE';
DBMS_OUTPUT.PUT_LINE(trim(V_ISIN_CODE)||' => ' ||V_ISSUE_INST_NAME||V_ISSUE_CNT||' 투자설명서 => https://dart.fss.or.kr/dsaf001/main.do?rcpNo='||V_FSS_NO);
EXCEPTION
WHEN  NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('존재하지않는코드:::'||&P_ISIN_CODE);
END;
/
