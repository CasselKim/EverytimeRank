from datetime import datetime
import time
from selenium import webdriver
from urllib import parse
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

from multiprocessing import Process

def rollon(number) :
    print('start!!!!')
    from bs4 import BeautifulSoup as bs
    from urllib.request import urlopen
    from selenium import webdriver
    import pandas as pd
    import os
    import numpy as np
    base_dir = "C:/Users/KIMSEONGROK/desktop"

    file_nm = "df{}.xlsx".format(number)
    xlxs_dir = os.path.join(base_dir, file_nm)

    options = webdriver.ChromeOptions()

    # headless 옵션 설정
    #options.add_argument('headless')
    #options.add_argument("no-sandbox")

    # 사람처럼 보이게 하는 옵션들
    options.add_argument("disable-gpu")  # 가속 사용 x
    options.add_argument("lang=ko_KR")  # 가짜 플러그인 탑재
    options.add_argument(
        'user-agent=Mozilla/5.0 \
        (Macintosh; Intel Mac OS X 10_12_6) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정

    driver = webdriver.Chrome('chromedriver', options=options)

    driver.implicitly_wait(3)

    result = pd.DataFrame(columns=['gallery','title','main','main_vote','best_comment','best_comment_vote','URL'])

    driver.delete_all_cookies()
    driver.get('https://knu.everytime.kr/hotarticle/p/1')

    driver.find_element_by_xpath(
    '//*[@id="container"]/form/p[1]/input'
    ).send_keys('id')

    driver.find_element_by_xpath(
    '//*[@id="container"]/form/p[2]/input'
    ).send_keys('password')

    driver.find_element_by_xpath(
    '//*[@id="container"]/form/p[3]/input'
    ).click()


    for i in range(number*89+1,number*89+89+1) :
        urls = []
        driver.get('https://knu.everytime.kr/hotarticle/p/'+str(i))

        for j in range(1,21) :
            urls.append(driver.find_element_by_xpath(
                '/html/body/div[2]/div[2]/article[{}]/a'.format(j)
            ).get_attribute('href'))

        for k,url in enumerate(urls) :
            driver.get(url)

            try :
                title = driver.find_element_by_xpath(
                    '/html/body/div[2]/div[2]/article/a/h2'
                ).text
            except :
                title='No Title'

            main = driver.find_element_by_xpath(
                '/html/body/div[2]/div[2]/article/a/p'
            ).text

            main_vote = driver.find_element_by_xpath(
                '/html/body/div[2]/div[2]/article/a/ul[2]/li[2]'
            ).text

            gallery = driver.find_element_by_xpath(
                '/html/body/div[2]/div[1]/h1/a'
            ).text


            comments = driver.find_elements_by_tag_name('article')
            best_comment='베스트코멘트 없음'
            best_vote = 0

            for comment in comments[1:] :
                vote = comment.find_element_by_class_name('status.commentvotestatus').text
                if len(vote) == 0 :
                    vote = 0
                else :
                    vote = int(vote)
                if vote > best_vote :
                    best_comment = comment.find_element_by_class_name('large').text
                    best_vote = vote
            #print([gallery, title, main, main_vote, best_comment, best_vote, url])
            result.loc[20*(i-1)+k] = [gallery, title, main, main_vote, best_comment, best_vote, url]

        result.to_excel(xlxs_dir, # directory and file name to write
                        sheet_name = 'Sheet1',
                        na_rep = 'NaN',
                        float_format = "%.2f",
                        header = True,
                        #columns = ["group", "value_1", "value_2"], # if header is False
                        index = True,
                        index_label = "id",
                        startrow = 1,
                        startcol = 1,
                        #engine = 'xlsxwriter',
                        freeze_panes = (2, 0)
                        )

if __name__ == '__main__' :
    p1 = Process(target=rollon, args=(0,))
    p2 = Process(target=rollon, args=(1,))
    p3 = Process(target=rollon, args=(2,))
    p4 = Process(target=rollon, args=(3,))
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
