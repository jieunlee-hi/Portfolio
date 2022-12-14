import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import numpy as np

#date_range함수 : 일정기간의 시간을 생성
#원하는 기간의 데이터 수집가능
dt_index = pd.date_range(start='20210801', end='20220801')
dt_list = dt_index.strftime('%Y%m%d').tolist()
print(dt_list)
all_data_frame=[]
append = all_data_frame.append
for i in dt_list:
    #수집데이터 url
    url = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=102&sid2=252&date=' + i
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}

    #페이지넘김 최대페이지 20
    for page in range(1,20):
        try:
            response = requests.get(url + '&page=' + str(page), headers=headers)
            html = response.text
            print(url)
            soup = BeautifulSoup(html, 'html.parser')
            #수집하고자하는 항목 추출(헤드라인)
            title = soup.select('#main_content > div.list_body.newsflash_body > ul > li > a')
            div = soup.find("div", "paging")

            # a태그만 추출
            result = []
            for a in div.find_all("a"):
                # headline추출및 headline 앞뒤 공백제거
                result.append(a.get_text())

            if len(result) == 0:
                paging = 0
            else :
                paging = result[-1]

            print(page)
            print(paging)
            if int(page) > int(paging)+int(1):
                break
            newsdate = i
            news_date = []
            news_title = []
            div = soup.find("div", "list_body")
            for title in div.find_all("a"):
                title = title.get_text()
                title = re.sub('\n|\t|', '', title).strip()
                # title=list(filter(None, title))
                news_title.append(title)
                news_date.append(newsdate)

            print(news_title)

            df = pd.DataFrame({"headline": news_title, "날짜": news_date})
            time.sleep(1)

            append(df)
            df_concat = pd.concat(all_data_frame, axis=0, ignore_index=False)
            #기사가 아닌 내용은 수집하지않음.
            df_concat = df_concat[
                (df_concat['headline'].str.contains('안내헤드라인')) | (df_concat['headline'].str.contains('더보기')) | (
                    df_concat['headline'].str.contains('오늘의 인사 종합')|df_concat['headline'].str.contains('동영상기사')) == False]

            df_concat['headline'].replace('', np.nan, inplace=True)
            new_df = df_concat.dropna(how='any')
            print(new_df)

            print(new_df.isnull().sum())
            # 엑셀파일로 저장하기
            writer = pd.ExcelWriter('1year_environment_issue.xlsx')
            new_df.to_excel(writer, sheet_name='Sheet1', index=False, header=False, na_rep=' ',
                        encoding='utf-16')  # 엑셀로 저장
            writer.save()

        except :
            pass



