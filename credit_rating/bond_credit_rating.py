# coding=utf-8
import requests
from io import BytesIO
import time
from datetime import datetime, timedelta
import sys, os, traceback
import xlwt
from selenium import webdriver
import pandas as pd
from datetime import datetime
import re
import openpyxl
from pandas import Series, DataFrame
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import warnings
# 오류 경고 무시하기
warnings.filterwarnings(action='ignore')
import glob
#사용자에따라 다운로드 경로수정
outpath = "C:\\Users\\user\\Downloads\\"


# 한기평 - 회사채
# 한기평사이트개편-220906 엑셀파일 다운로드받아 그 안에서 데이터 입수형식으로 코드수정
#엑셀다운코드
def kap_bond_excel():
    # 옵션 생성
    options = webdriver.ChromeOptions()
    # 창 숨기는 옵션 추가
    #options.add_argument("headless")
    driver = webdriver.Chrome('C:\credit\chromedriver_win32\chromedriver.exe',options=options)
    # 암묵적으로 웹 자원 로드를 위해 최대 60초까지 기다려 준다.

    driver.implicitly_wait(60)

    driver.get('http://www.korearatings.com/cms/frCmnCon/index.do?MENU_ID=360')
    time.sleep(2)


    # 엑셀파일 다운로드
    down = driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div/button[3]').send_keys(Keys.ENTER)
    time.sleep(3)

    driver.close()

#한기평데이터추출
def kap_bond_master():
    try :
        files=glob.glob(outpath+'등급*.xlsx')
        #print(files[0])
        df = pd.read_excel(files[0], sheet_name='회사채',skiprows=[0,1,2],thousands = ',')
        #print(df)
        df.columns = ['회사명', '종류', '구분', '회차', '발행액', '직전등급(Outlook)', '현재등급(Outlook)', '평가일', '공시일']
        # 필요한 컬럼만 선택
        df = df[['회사명', '회차', '구분', '직전등급(Outlook)', '현재등급(Outlook)', '평가일', '발행액']]
        # 현재등급과 Outlook 항목을 분리하기 위해 컬럼 한개를 현재Outlook 라는 이름으로 추가한다
        df = df.assign(현재Outlook=df['현재등급(Outlook)'])
        # 직전등급과 Outlook 항목을 분리하기 위해 컬럼 한개를 직전Outlook 라는 이름으로 추가한다
        df = df.assign(직전Outlook=df['직전등급(Outlook)'])
        # 신용평가기관
        df = df.assign(신용평가기관=3)
        # 종목코드
        df = df.assign(종목코드='')
        # 데이터종류
        df = df.assign(데이터종류=11)

        # 날짜 원본형식(YYYY.MM.DD)을 변경(YYYYMMDD)
        df['평가일'] = df['평가일'].str.replace('.', '',regex=True)
        df['현재등급(Outlook)'] = df['현재등급(Outlook)'].str.replace('(', '|',regex=True).str.replace(')', '',regex=True).str.replace('↓','',regex=True).str.replace('↑','',regex=True).str.split('|').str[0]
        df['현재Outlook'] = df['현재Outlook'].str.replace('(', '|',regex=True).str.replace(')', '',regex=True).str.split('|').str[1].str.replace('안정적', '1',regex=True).str.replace('긍정적', '2',regex=True).str.replace('부정적', '3',regex=True).str.replace('유동적', '4',regex=True).str.replace('없음', '5',regex=True)
        df['구분'] = df['구분'].str.replace('본', '21', regex=True).str.replace('정기', '22', regex=True).str.replace('수시', '23',
                                                                                                               regex=True)

        #직전등급(Outlook)에 아무것도 값이 없는 경우, 한칸공백으로 치환한다
        if str(df['직전등급(Outlook)'][0]) == 'nan':
            df['직전등급(Outlook)'] = ' '
            df['직전Outlook'] = ' '
        else:
            df['직전등급(Outlook)'] = df['직전등급(Outlook)'].str.replace('(', '|',regex=True).str.replace(')', '',regex=True).str.replace('↓','',regex=True).str.replace('↑','',regex=True).str.split('|').str[0]
            df['직전Outlook'] = df['직전Outlook'].str.replace('(', '|',regex=True).str.replace(')', '',regex=True).str.split('|').str[1].str.replace\
            ('안정적', '1',regex=True).str.replace('긍정적', '2',regex=True).str.replace('부정적', '3',regex=True).str.replace('유동적', '4',regex=True).str.replace('없음', '5',regex=True)

        # DB 컬럼 정의 순서대로 맞춤
        df = df[['평가일', '신용평가기관', '회차', '회사명', '종목코드', '발행액', '현재등급(Outlook)', '구분', '현재Outlook', '데이터종류', '직전등급(Outlook)',
             '직전Outlook']]
        print(df)
        # 평가일 조건
        today = datetime.today().strftime('%Y%m%d')
        df = df[df['평가일'] == today]

        # 색인과 컬럼은 파일에 저장하지 않음. 구분자는 |. 누락값은 한칸공백으로 치환.
        # df.to_csv('kap_bond.csv',index=False,header=False,sep='|',na_rep=' ',encoding='utf-16')
    except AttributeError:
        df = DataFrame(columns=('평가일', '신용평가기관', '회차', '회사명', '종목코드', '발행액', '현재등급(Outlook)', '구분', '현재Outlook', '데이터종류', '직전등급(Outlook)',
             '직전Outlook'))
        return df
    except ValueError:
        df = DataFrame(columns=('평가일', '신용평가기관', '회차', '회사명', '종목코드', '발행액', '현재등급(Outlook)', '구분', '현재Outlook', '데이터종류', '직전등급(Outlook)',
             '직전Outlook'))
        return df
    except IndexError:
        df = DataFrame(columns=('평가일', '신용평가기관', '회차', '회사명', '종목코드', '발행액', '현재등급(Outlook)', '구분', '현재Outlook', '데이터종류', '직전등급(Outlook)',
             '직전Outlook'))
        return df
    return df
#다운받은엑셀삭제
def EXCEL_DELETE():
    # 작업디렉토리
    [os.remove(f) for f in glob.glob(outpath+'등급*.xlsx')]


# 한신평 - 회사채
# 다운로드된 파일(등급공시(오늘일자).xls)의 확장자가 .xls 이지만 실제 내용을 보면 HTML 문서 이다.
# GET방식
def kis_bond_master():
    try:
        today = datetime.today()
        today = today.strftime('%Y%m%d')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        driver = webdriver.Chrome('C:\\credit\chromedriver_win32\chromedriver.exe', chrome_options=chrome_options)

        url = 'https://www.kisrating.com/ratings/hot_disclosure.do'
        # print(url)
        driver.get(url)
        # start = driver.find_element_by_xpath('//*[@id="startDt"]')
        # actionChains2 = ActionChains(driver)
        # actionChains2.double_click(start).perform()
        # start.send_keys('20200130')
        # time.sleep(2)
        # driver.find_element_by_xpath('//*[@id="btnSearch"]').send_keys(Keys.ENTER)
        # time.sleep(5)
        cnt = driver.find_element_by_xpath('//*[@id="view1"]/div[1]/h2/span/em')
        cnt = cnt.text
        #print(cnt)

        all_data_frame = []
        for i in range(1, int(cnt) + int(cnt), 2):

            # 평가일
            item1 = driver.find_element_by_xpath('//*[@id="debentureList"]/tbody/tr[' + str(i) + ']/td[11]')
            item1 = item1.text

            # 날짜 포맷변경
            date = datetime.strptime(item1, '%Y.%m.%d')
            date1 = datetime.strftime(date, '%Y%m%d')

            # 회차
            item2 = driver.find_element_by_xpath('//*[@id="debentureList"]/tbody/tr[' + str(i) + ']/td[4]')
            # print(item2.text)

            # 회사명
            item3 = driver.find_element_by_xpath('//*[@id="debentureList"]/tbody/tr[' + str(i) + ']/td[2]')
            # print(item3.text)

            # 발행액
            item4 = driver.find_element_by_xpath('//*[@id="debentureList"]/tbody/tr[' + str(i) + ']/td[5]')
            # print(item4.text)
            item4 = re.sub(',', '', item4.text, 0).strip()
            # 현재등급
            item5 = driver.find_element_by_xpath('//*[@id="debentureList"]/tbody/tr[' + str(i) + ']/td[10]')
            # print(item5.text)

            # 평가구분
            item6 = driver.find_element_by_xpath('//*[@id="debentureList"]/tbody/tr[' + str(i) + ']/td[7]')
            # print(item6.text)
            item6 = item6.text
            item6 = item6.replace("본", "21")
            item6 = item6.replace("정기", "22")
            item6 = item6.replace("수시", "23")

            # 현재Outlook
            item7 = driver.find_element_by_xpath('//*[@id="debentureList"]/tbody/tr[' + str(i + 1) + ']/td[3]')
            # print(item7.text)
            item7 = item7.text
            item7 = item7.replace("안정적", "1")
            item7 = item7.replace("긍정적", "2")
            item7 = item7.replace("부정적", "3")
            item7 = item7.replace("유동적", "4")
            item7 = item7.replace("없음", "5")

            # 직전등급
            item8 = driver.find_element_by_xpath('//*[@id="debentureList"]/tbody/tr[' + str(i) + ']/td[8]')
            # print(item8.text)
            # 직전 outlook
            item9 = driver.find_element_by_xpath('//*[@id="debentureList"]/tbody/tr[' + str(i + 1) + ']/td[1]')
            item9 = item9.text
            item9 = item9.replace("안정적", "1")
            item9 = item9.replace("긍정적", "2")
            item9 = item9.replace("부정적", "3")
            item9 = item9.replace("유동적", "4")
            item9 = item9.replace("없음", "5")

            # print(item9.text)
            # print(date1)
            if date1 == today:
                data = {'신용평가일': [date1],
                        '신용평가기관': '1',
                        '발행횟수': [item2.text],
                        '한글회사명': [item3.text],
                        '종목코드': '',
                        '발행금액': [item4],
                        '신용평가등급': [item5.text],
                        '신용평가종류': [item6],
                        'OUTLOOKRATING': [item7],
                        '데이터종류': '11',
                        '직전등급': [item8.text],
                        '직전OUTLOOKRATING': [item9]
                        }

                df = pd.DataFrame(data,
                                  columns=['신용평가일', '신용평가기관', '발행횟수', '한글회사명', '종목코드', '발행금액', '신용평가등급', '신용평가종류',
                                           'OUTLOOKRATING',
                                           '데이터종류', '직전등급', '직전OUTLOOKRATING'])
                all_data_frame.append(df)
        df_concat = pd.concat(all_data_frame, axis=0, ignore_index=False)
        #print(df_concat)
        return df_concat

    except AttributeError:
        df_concat = DataFrame(columns=('신용평가일', '신용평가기관', '발행횟수', '한글회사명', '종목코드', '발행금액', '신용평가등급', '신용평가종류', 'OUTLOOKRATING',
                                            '데이터종류', '직전등급', '직전OUTLOOKRATING'))
        return df_concat
    except ValueError:
        df_concat = DataFrame(columns=('신용평가일', '신용평가기관', '발행횟수', '한글회사명', '종목코드', '발행금액', '신용평가등급', '신용평가종류', 'OUTLOOKRATING',
                                            '데이터종류', '직전등급', '직전OUTLOOKRATING'))
        return df_concat




# 한신정 - 회사채
# 다운로드된 파일(일일등급속보_오늘일자.xls)의 확장자가 .xls 이므로 EXCEL 문서 이다.
# GET방식
def nice_bond_master():
    today = datetime.today().strftime('%Y-%m-%d')
    secuTyp = 'BOND'
    strDate = today
    endDate = today
    url = 'http://www.nicerating.com/disclosure/dayRatingPoiExcel.do?today=' + today + '&cmpCd=&seriesNm=&secuTyp=' + secuTyp + '&strDate=' + strDate + '&endDate=' + endDate

    r = requests.get(url, stream=True)
    dfs = pd.read_excel(BytesIO(r.content), header=0, thousands=',')
    # 컬럼헤더명 정의
    dfs.columns = ['기업명', '회차', '종류', '평정', '직전등급', '직전전망', '현재등급', '현재전망', '등급결정일', '등급확정일', '발행액(억원)']
    # 필요한 컬럼만 선택
    dfs = dfs[['기업명', '회차', '평정', '직전등급', '직전전망', '현재등급', '현재전망', '등급확정일', '발행액(억원)']]
    # df = dfs[0].copy()
    # 신용평가기관
    dfs = dfs.assign(신용평가기관=2)
    # 종목코드
    dfs = dfs.assign(종목코드='')
    # 데이터종류
    dfs = dfs.assign(데이터종류=11)

    # 날짜 원본형식(YYYY.MM.DD)을 변경(YYYYMMDD)
    dfs['등급확정일'] = dfs['등급확정일'].str.replace('.', '')
    dfs['현재등급'] =dfs['현재등급'].str.replace('↓','').str.replace('↑','')
    dfs['직전등급'] =dfs['직전등급'].str.replace('↓','').str.replace('↑','')
    dfs['현재전망'] = dfs['현재전망'].str.replace('Stable', '1').str.replace('Positive', '2').str.replace('Negative','3').str.replace('Developing', '4').str.replace('None', '5')
    dfs['직전전망'] = dfs['직전전망'].str.replace('Stable', '1').str.replace('Positive', '2').str.replace('Negative','3').str.replace('Developing', '4').str.replace('None', '5')
    dfs['평정'] = dfs['평정'].str.replace('본', '21').str.replace('정기', '22').str.replace('수시', '23')

    # 첫번째,두번째 행이 병합되어서 세번째 행부터 보여준다
    dfs = dfs[2:len(dfs)]
    # DB 컬럼 정의 순서대로 맞춤
    dfs = dfs[['등급확정일', '신용평가기관', '회차', '기업명', '종목코드', '발행액(억원)', '현재등급', '평정', '현재전망', '데이터종류', '직전등급', '직전전망']]
    # 색인과 컬럼은 파일에 저장하지 않음. 구분자는 |. 누락값은 한칸공백으로 치환.
    # dfs.to_csv('nice_bond.csv',index=False,header=False,sep='|',na_rep=' ',encoding='utf-16')

    return dfs


try:
    # 이전에 에러가 기록된 파일은 삭제한다.
    os.unlink('bond_cred_error.txt')
except:
    pass

try :
    kap_bond_excel()
    time.sleep(1)
    dfm_kap = kap_bond_master()
    dfm_nice = nice_bond_master()
    dfm_kis = kis_bond_master()

    # 3개 평가사의 각 헤더명이 다르므로, 합치기 전 동일하게 맞춰준다.
    dfm_kap.columns = ['신용평가일', '신용평가기관', '발행횟수', '한글회사명', '종목코드', '발행금액', '신용평가등급', '신용평가종류', 'OUTLOOKRATING',
                       '데이터종류', '직전등급', '직전OUTLOOKRATING']

    dfm_nice.columns = ['신용평가일', '신용평가기관', '발행횟수', '한글회사명', '종목코드', '발행금액', '신용평가등급', '신용평가종류', 'OUTLOOKRATING',
                        '데이터종류', '직전등급', '직전OUTLOOKRATING']
    dfm_kis.columns = ['신용평가일', '신용평가기관', '발행횟수', '한글회사명', '종목코드', '발행금액', '신용평가등급', '신용평가종류', 'OUTLOOKRATING',
                       '데이터종류', '직전등급', '직전OUTLOOKRATING']
    dfm_all = pd.concat([dfm_kap, dfm_nice,dfm_kis])
    # 3개 평가사의 결과를 합쳐 파일로 저장한다
    # dfm_all.to_csv('grade_bond.csv', index=False, header=False, sep='|', na_rep=' ', encoding='utf-16')
    writer = pd.ExcelWriter('grade_bond.xls')
    dfm_all.to_excel(writer, sheet_name='Sheet1', index=False, header=False, na_rep=' ', encoding='utf-16')
    writer.save()
    #EXCEL_DELETE()




except:
    #에러가 발생한 경우 StackTrace를 파일로 기록한다.
    outputFile = open('bond_cred_error.txt', 'w')
    traceback.print_exc(file=outputFile)
    outputFile.close()