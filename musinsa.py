import os
import time
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import urllib.request

class musinsa_crw:
    def __init__(self, category, URL, clothes, page_len, driver):
        self.category = category
        self.URL = URL
        self.clothes = clothes
        self.page_len = page_len
        self.driver = driver

    # 상품 진열 페이지에서 정보 페이지의 새 탭을 열어 원본 이미지 다운로드
    def crawling(self, page):
        i = 1
        while True:
            try:
                # 상품 정보 페이지 열기
                target = self.driver.find_element_by_css_selector(f'#searchList > li:nth-child({i}) > div.li_inner > div.list_img > a')
                target.send_keys(Keys.CONTROL+'\n')
                
                # 정보 페이지로 이동
                self.driver.switch_to.window(driver.window_handles[1])  

                # 원본 이미지 다운로드
                elements = self.driver.find_element_by_xpath('//*[@id="bigimg"]').get_attribute('src')
                urllib.request.urlretrieve(elements, os.path.join("musinsa_img", self.clothes, self.clothes+"_"+str(page)+"_"+str(i)+ ".jpg")) 

                # 정보 페이지 닫고 진열 페이지로 이동
                self.driver.close()
                self.driver.switch_to.window(driver.window_handles[0])
                i += 1
            except:
                print(f'--{page} 페이지 완료--')
                break

    # 진열 페이지 넘기기
    def loop_page(self, pages):
        for page in range(1, pages + 1):
            page_number = page % 10 + 2  # 3에서 

            # 팝업 생성 시 제거 후 진행
            time.sleep(3)
            try:
                pop_up = self.driver.find_element_by_css_selector("body > div.ab-iam-root.v3.ab-animate-in.ab-animate-out.ab-effect-modal.ab-show > div.ab-in-app-message.ab-background.ab-modal-interactions.ab-modal.ab-centered > button > svg")
                pop_up.click()
                print("팝업 제거")

            except NoSuchElementException:
                print("팝업 없음")

            # 1부터 9까지 이동 
            if page_number != 2:
                self.driver.find_element_by_css_selector(f'#goods_list > div.boxed-list-wrapper > div.sorter-box.box > div > div > a:nth-child({page_number})').click()
                self.crawling(page)

            # page_number가 2일 경우 10 페이지 이동 후 "다음" 클릭
            else:
                self.driver.find_element_by_css_selector('#goods_list > div.boxed-list-wrapper > div.sorter-box.box > div > div > a:nth-child(12)').click() # 10 페이지
                self.crawling(page)
                self.driver.find_element_by_css_selector('#goods_list > div.boxed-list-wrapper > div.sorter-box.box > div > div > a:nth-child(13)').click() # 다음 페이지

        print("크롤링 종료")    
        self.driver.close()


    def page_select(self):   
        self.driver.implicitly_wait(3)
        self.driver.get(self.URL + self.category[self.clothes])
        self.clothes = self.clothes.replace(' ', '_')
        os.makedirs("musinsa_img/" + self.clothes, exist_ok = True)

        # 총 페이지 수와 크롤링 할 페이지 수 비교 
        max_number = self.driver.find_element_by_xpath('//*[@id="goods_list"]/div[2]/div[2]/span[8]/span[1]')
        max_page = int(max_number.text)  
        
        if max_page < self.page_len:
            print(f"페이지 수가 적어 {max_page} 페이지까지 크롤링 합니다.")
            self.loop_page(max_page)
        else:
            print(f"{self.page_len} 페이지까지 크롤링 합니다.")
            self.loop_page(self.page_len)


category = {"반팔티":"001001", "셔츠,블라우스":"001002", "카라티":"001003",
            "후드티":"001004", "맨투맨":"001005", "니트 스웨터":'001006',
            "기타 상의":"001008", "긴팔티":"001010", "후드 집업":"002022", "블루종":"002001",
            "레더 재킷":"002002", "무스탕":"002025", "트러커 재킷":"002017",
            "블레이저 재킷":"002003", "가디건":"002020", "플리스":"002023",
            "트레이닝 재킷":"002018", "바시티 재킷":"002004", "환절기 코트":"002008", "싱글 코트":"002007",
            "더블 코트":"002024", "롱패딩":"002013", "숏패딩":"002012", "코치(나일론) 재킷":"002006",
            "데님 팬츠":"003002", "숏팬츠":"003009", "코튼 팬츠":"003007", "레깅스":"003005",
            "슬랙스":"003008", "트레이닝 팬츠":"003004", "기타 바지":"003006"}            


print('''
-----------------------카테고리------------------------------
티셔츠: 반팔티, 긴팔티, 카라티, 후드티, 니트 스웨터, 맨투맨

재킷: 후드 집업, 블루종, 레더 재킷, 무스탕, 트러커 재킷, 
         트레이닝 재킷, 바시티 재킷, 블레이저 재킷,
         가디건, 플리스, 코치(나일론) 재킷
         
코트: 환절기 코트, 싱글 코트, 더블 코트

패딩: 롱패딩, 숏패딩

하의: 데님 팬츠, 숏팬츠, 코튼 팬츠, 레깅스,
      슬랙스, 트레이닝 팬츠

기타: 기타 상의, 기타 바지
-------------------------------------------------------------
''')


clothes = input("가져올 의류: ")
page_len = int(input("페이지 수 (한 페이지에 90개): "))

URL = 'https://www.musinsa.com/category/'
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome('C:\\Users\\user\\workspace\\chromedriver\\chromedriver.exe', chrome_options = options)

musinsa = musinsa_crw(category, URL, clothes, page_len, driver)
musinsa.page_select()

