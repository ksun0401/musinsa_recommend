import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request

# 이전 페이지로 돌아가는 driver.back()과 driver.execute_script("window.history.go(-1)") 함수가 작동이 안 된다.

category = {"반소매 티셔츠":"001001", "셔츠/블라우스":"001002", "피케/카라티 셔츠":"001003",
            "후드 티셔츠":"001004", "맨투맨/스웨트 셔츠":"001005", "니트/스웨터":'001006',
            "기타 상의":"001008", "긴소매 티셔츠":"001010", "후드 집업":"002022", "블루종/MA-1":"002001",
            "레더/라이더스 재킷":"002002", "무스탕/퍼":"002025", "트러커재킷":"002017",
            "슈트/블레이저 재킷":"002003", "가디건":"002020", "플리스/뽀글이":"002023",
            "트레이닝 재킷":"002018", "바시티 재킷":"002004", "환절기코트":"002008", "싱글 코트":"002007",
            "더블 코트":"002024", "롱패딩":"002013", "숏패딩":"002012", "나일론/코치 재킷":"002006",
            "데님 팬츠":"003002", "숏팬츠":"003009", "코튼 팬츠":"003007", "레깅스":"003005",
            "슬랙스":"003008", "트레이닝/조거 팬츠":"003004", "기타 바지":"003006"}


class musinsa_crw():
    def __init__(self, category, URL, clothes):
        self.category = category
        self.URL = URL
        self.clothes = clothes
    
    def crw(self):
        driver = webdriver.Chrome('C:\\Users\\user\\workspace\\chromedriver\\chromedriver.exe')
        driver.implicitly_wait(3)
        driver.get(self.URL + self.category[self.clothes])
        self.clothes = self.clothes.replace(' ', '_')
        os.makedirs("musinsa_img/" + self.clothes, exist_ok = True)
        num = 1
        while True:
            # try:
            driver.find_element_by_css_selector(f'#searchList > li:nth-child({num}) > div.li_inner > div.list_img > a > img').click()
            time.sleep(3)
            # elements = driver.find_element_by_xpath('//*[@id="bigimg"]').get_attribute('src')
            # urllib.request.urlretrieve(elements, os.path.join("musinsa_img", self.clothes, self.clothes + "_" + str(num) + ".jpg"))
            # driver.find_element_by_xpath('/html/body/div[15]/div[2]/button/svg').click
            driver.back() 
            num += 1
            # except:
            #     print("크롤링 종료")
            #     break
            # driver.close()

clothes = input("검색할 옷:")
URL = 'https://www.musinsa.com/category/'

musinsa = musinsa_crw(category, URL, clothes)
musinsa.crw()







#searchList > li:nth-child(1) > div.li_inner > div.list_img > a > img
#searchList > li:nth-child(2) > div.li_inner > div.list_img > a > img

