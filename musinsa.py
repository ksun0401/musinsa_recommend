import os
import time
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request

category = {"반소매 티셔츠":"001001", "셔츠/블라우스":"001002", "피케/카라티 셔츠":"001003",
            "후드 티셔츠":"001004", "맨투맨/스웨트 셔츠":"001005", "니트/스웨터":'001006',
            "기타 상의":"001008", "긴소매 티셔츠":"001010", "후드 집업":"002022", "블루종/MA-1":"002001",
            "레더/라이더스 재킷":"002002", "무스탕/퍼":"002025", "트러커재킷":"002017",
            "슈트/블레이저 재킷":"002003", "가디건":"002020", "플리스/뽀글이":"002023",
            "트레이닝 재킷":"002018", "바시티 재킷":"002004", "환절기코트":"002008", "싱글 코트":"002007",
            "더블 코트":"002024", "롱패딩":"002013", "숏패딩":"002012", "나일론/코치 재킷":"002006",
            "데님 팬츠":"003002", "숏팬츠":"003009", "코튼 팬츠":"003007", "레깅스":"003005",
            "슬랙스":"003008", "트레이닝/조거 팬츠":"003004", "기타 바지":"003006"}            

class musinsa_crw:
    def __init__(self, category, URL, clothes, img_len, driver):
        self.category = category
        self.URL = URL
        self.clothes = clothes
        self.img_len = img_len
        self.driver = driver
         
    def img_crw(self, page):
        i = 1
        while True:
            try:
                target = self.driver.find_element_by_css_selector(f'#searchList > li:nth-child({i}) > div.li_inner > div.list_img > a')
                target.send_keys(Keys.CONTROL+'\n')
                self.driver.switch_to.window(driver.window_handles[1])
                elements = self.driver.find_element_by_xpath('//*[@id="bigimg"]').get_attribute('src')
                urllib.request.urlretrieve(elements, os.path.join("musinsa_img", self.clothes, self.clothes+"_"+str(page)+"_"+str(i)+ ".jpg")) 
                self.driver.close()
                self.driver.switch_to.window(driver.window_handles[0])
                i += 1
            except:
                print(f'--{page} 페이지 완료--')
                break

    def loop_page(self, pages):
        for page in range(1, pages + 1):
            page_number = page % 10 + 2
            try:
                if page_number != 2:
                    self.driver.find_element_by_css_selector(f'#goods_list > div.boxed-list-wrapper > div.sorter-box.box > div > div > a:nth-child({page_number})').click()
                    self.img_crw(page)
                else:
                    self.driver.find_element_by_css_selector('#goods_list > div.boxed-list-wrapper > div.sorter-box.box > div > div > a:nth-child(12)').click()
                    self.img_crw(page)
                    self.driver.find_element_by_css_selector('#goods_list > div.boxed-list-wrapper > div.sorter-box.box > div > div > a:nth-child(13)').click()
            except:
                print("-------크롤링 종료--------")
                break

    def pass_page(self):   
        self.driver.implicitly_wait(3)
        self.driver.get(self.URL + self.category[self.clothes])
        self.clothes = self.clothes.replace(' ', '_')
        os.makedirs("musinsa_img/" + self.clothes, exist_ok = True)

        max_number = self.driver.find_element_by_xpath('//*[@id="goods_list"]/div[2]/div[2]/span[8]/span[1]')
        max_page = int(max_number.text)  
        pages = int(self.img_len/90) + 1
        
        if max_page <= pages:
            print(f"이미지 수가 적어 {max_page} 페이지까지 크롤링 합니다.")
            self.loop_page(max_page)
        else:
            print(f"{pages} 페이지까지 크롤링 합니다.")
            self.loop_page(pages)


clothes = input("검색할 옷: ")

img_len = int(input("다운로드 이미지 수: "))
URL = 'https://www.musinsa.com/category/'
driver = webdriver.Chrome('C:\\Users\\user\\workspace\\chromedriver\\chromedriver.exe')

musinsa = musinsa_crw(category, URL, clothes, img_len, driver)
musinsa.pass_page()