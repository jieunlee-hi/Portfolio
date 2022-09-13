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

    CURSOR join_cur --Ŀ������
    IS
    select * from
    (SELECT FSS_NO , ISSUE_INST_NAME, ISSUE_NAME ,
    CASE WHEN REPLACE(issue_name,' ','') LIKE '%�ְ���������%' OR
    REPLACE(issue_name,' ','') LIKE '%�ְ������Ļ���������%'  OR
    REPLACE(issue_name,' ','') LIKE '%ELS%' THEN 'ELS'
    WHEN REPLACE(issue_name,' ','') LIKE '%�Ļ���������%' OR 
    REPLACE(issue_name,' ','') LIKE '%��Ÿ�Ļ���������%' THEN 'DLS'
    WHEN REPLACE(issue_name,' ','') LIKE '%�ְ������Ļ����ջ�ä%'OR
    REPLACE(issue_name,' ','') LIKE '%ELB%' THEN 'ELB'
    WHEN REPLACE(issue_name,' ','') LIKE '%��Ÿ�Ļ����ջ�ä%' OR 
    REPLACE(issue_name,' ','') LIKE '%�Ļ����ջ�ä%' OR
    REPLACE(issue_name,' ','') LIKE '%DLB%' THEN 'DLB'	
    ELSE 'N/A' END AS goodtype
    FROM DARTFSS)a 
    join SEIBRO_TMP on  a.issue_name LIKE '%'||trim(SEIBRO_TMP.issue_cnt)||'%'
    where  a.issue_inst_name =SEIBRO_TMP.issue_inst_name
    and SEIBRO_TMP.good_type = a.goodtype;


BEGIN
    OPEN join_cur;
    
    LOOP --�ݺ�
        FETCH join_cur INTO FSS_NO,issue_inst_name,issue_name,goodtype,ISIN_CODE,good_type,issue_inst_name_1,issue_cnt; --Ŀ������ ������ �����ͼ� �ϳ��� ������ �ֱ�
        EXIT WHEN join_cur %NOTFOUND; --���̻� ���� ��� ����
            --DBMS_OUTPUT.ENABLE(NULL); 
            --DBMS_OUTPUT.PUT_LINE(FSS_NO||'  '||ISIN_CODE||' '||issue_inst_name||' '||issue_cnt||' '||goodtype); --��¹�
            --�ٸ����̺� Ŀ��������insert
            insert into matching_result values(FSS_NO,ISIN_CODE,ISSUE_INST_NAME,ISSUE_CNT); 
    END LOOP;
    CLOSE join_cur; --Ŀ�� �ݱ�
END;
end DARTS2SEIBRO;