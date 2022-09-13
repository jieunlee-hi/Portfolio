create or replace PROCEDURE SEIBRO_result
IS
BEGIN
DECLARE
--���� ����
    ISSUE_INST_NAME SEIBRO.issue_inst_name%TYPE;
    ISIN_CODE SEIBRO.ISIN_CODE%TYPE;
    ISSUE_NAME_SEIBRO SEIBRO.ISSUE_NAME_SEIBRO%TYPE;
    GOODS_TYPE SEIBRO.GOODS_TYPE%TYPE;
    ISSUE_DATE SEIBRO.ISSUE_DATE%TYPE;
    EXPIRY_DATE SEIBRO.EXPIRY_DATE%TYPE;
    FUND_TYPE SEIBRO.FUND_TYPE%TYPE;
    ISSUE_CNT char(1000);
    CURSOR seibro_cur --Ŀ������
    IS
    SELECT ISIN_CODE
			 , GOODS_TYPE --�Ļ��������� type ���
			 , TRIM(REPLACE(ISSUE_NAME_SEIBRO,' ','')) ISSUE_NAME_SEIBRO --ȸ�� ���� �����
             ,ISSUE_INST_NAME --����� 
             ,TO_NUMBER(REGEXP_REPLACE(REPLACE(ISSUE_NAME_SEIBRO,'100��',''), '[^0-9]', '')) ISSUE_CNT --����ȸ���� ����
			 , ISSUE_DATE --������
          FROM SEIBRO  
         WHERE GOODS_TYPE IN ('ELS','DLS','DLB','ELB')  					-- ELS/DLS/DLB/ELB
           AND FUND_TYPE != '���'							-- ��� ���� (���ڼ����� ���� ����)
           order by 4,5,6 desc
    ;

BEGIN
    OPEN seibro_cur;
    delete from seibro_tmp;
    LOOP --�ݺ�
        -- Ŀ������ ������ �����ͼ� �ϳ��� ������ �ֱ�
        FETCH seibro_cur INTO ISIN_CODE,GOODS_TYPE,ISSUE_NAME_SEIBRO,ISSUE_INST_NAME,ISSUE_CNT,ISSUE_DATE; 

            --DBMS_OUTPUT.ENABLE(NULL); --������Ѿ���
            --��¹�
            --DBMS_OUTPUT.PUT_LINE(ISIN_CODE||'  '||GOODS_TYPE||' '||ISSUE_INST_NAME||' '||ISSUE_CNT); 
            --�ٸ����̺� Ŀ��������insert
            insert into seibro_tmp values(ISIN_CODE,GOODS_TYPE,ISSUE_INST_NAME,ISSUE_CNT); 
            EXIT WHEN seibro_cur %NOTFOUND; --���̻� ���� ��� ����
    END LOOP;
    CLOSE seibro_cur; --Ŀ�� �ݱ�
END;
end SEIBRO_result;


exec SEIBRO_result;