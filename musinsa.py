import os
import time
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request

# 해결한 부분 -> driver.back() 뒤로 보내기를 새 탭 생성으로 대체
# 해결해야 할 부분 -> 페이지 넘기기, 저장 할 수 만큼 저장하기

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
    def __init__(self, category, URL, clothes, img_len):
        self.category = category
        self.URL = URL
        self.clothes = clothes
        self.img_len = img_len
    
    def crw(self):
        
        driver = webdriver.Chrome('C:\\Users\\user\\workspace\\chromedriver\\chromedriver.exe')
        driver.implicitly_wait(3)
        driver.get(self.URL + self.category[self.clothes])
        self.clothes = self.clothes.replace(' ', '_')
        os.makedirs("musinsa_img/" + self.clothes, exist_ok = True)
        pages = int((self.img_len-1)/90) + 1
        page_count = 1

        img_list = []
        while True:
            for i in range(3, 13):
                driver.find_element_by_css_selector(f'#goods_list > div.boxed-list-wrapper > div.sorter-box.box > div > div > a:nth-child({i})').click()
                page_num = 1
                for _ in range(img_len):
                    try:
                        target = driver.find_element_by_css_selector(f'#searchList > li:nth-child({page_num}) > div.li_inner > div.list_img > a')
                        target.send_keys(Keys.CONTROL+'\n')
                        driver.switch_to.window(driver.window_handles[1])
                        
                        elements = driver.find_element_by_xpath('//*[@id="bigimg"]')
                        img_list.append(elements.get_attribute('src'))
                        # urllib.request.urlretrieve(elements, os.path.join("musinsa_img", self.clothes, self.clothes+"_"+str(page_count)+"_"+str   page_num)+ ".jpg")) 
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        page_num += 1

                    except:
                        print("-------크롤링 종료-------")
                        break
                page_count += 1 
            if page_count == pages:
                break
    
        for i in range(img_list):
            urllib.request.urlretrieve(img_list[i], os.path.join("musinsa_img", self.clothes, self.clothes+"_"+str(i)+ ".jpg"))

    # def save_img(self):
    #     img_list = []
    #     crw(img_list)
    
    #     for i in range(img_list):
    #         urllib.request.urlretrieve(img_list[i], os.path.join("musinsa_img", self.clothes, self.clothes+"_"+str(i)+ ".jpg"))


clothes = input("검색할 옷: ")
img_len = int(input("다운로드 이미지 수: "))
URL = 'https://www.musinsa.com/category/'

musinsa = musinsa_crw(category, URL, clothes, img_len)
musinsa.crw()