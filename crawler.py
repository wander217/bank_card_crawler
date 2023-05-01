from selenium.webdriver import Chrome
from selenium.webdriver.chrome import options
from selenium.webdriver.common.by import By
import time
import re
from urllib import request
import os
import pandas as pd

class BankCardCrawler:
    def __init__(self) -> None:
       self.url = 'https://thebank.vn/the-tin-dung.html'
       option = options.Options()
       
      # thiết lập driver
       self.driver = Chrome(r'.\driver\chromedriver.exe', options=option)
       self.save_path = r'.\card_info.xlsx'
       self.sleep_time = 2
       
       #tạo folder lưu image
       if not os.path.exists(".\image"):
            os.mkdir(".\image")

    def process_money(self, txt):
        # chuyển từ chữ thành số
        num, unit = txt.split(" ")
        if unit.lower() == 'triệu': 
            return int(num) * 10**6
        if unit.lower() == 'tỷ': 
            return int(num) * 10**9

    def do_crawl(self):
        # Truy cập vào url
        self.driver.get(self.url)
        
        # Dừng hành động trong 2s (sleep_time=2)
        time.sleep(self.sleep_time)
        
        # Lấy tên ngân hàng qua xpath rồi lưu lại dưới dạng excel
        self.driver.find_element(By.XPATH, r'/html/body/main/div[4]/div[2]/ul/li[6]/button').click()
        bank_xpath = r'/html/body/div[9]'
        banks = self.driver.find_element(By.XPATH, bank_xpath).find_elements(By.TAG_NAME, 'label')
        bank_list = [[
            int(bank.find_element(By.TAG_NAME, 'input').get_attribute('value')), 
            bank.text
        ] for bank in banks]
        df = pd.DataFrame(data=bank_list, columns=[
            'id', 'Bank_name'
        ])
        df.to_excel(r'.\bank.xlsx', engine='openpyxl', index=False)
        
        #Lấy tên các loại thẻ qua xpath rồi lưu lại dưới dạng excel
        self.driver.find_element(By.XPATH, r'//*[@id="type_card_chosen"]').click()
        card_type_xpath = r'//*[@id="type_card_chosen"]/div/ul'
        card_types = self.driver.find_element(By.XPATH, card_type_xpath).find_elements(By.TAG_NAME, 'li')
        card_type_list = [[
            int(card_type.get_attribute('data-option-array-index')), 
            card_type.text
        ] for card_type in card_types][1:]
        df = pd.DataFrame(data=card_type_list, columns=[
            'id', 'Card_type'
        ])
        df.to_excel(r'.\card_type.xlsx', engine='openpyxl', index=False)
        
        # Duyệt từng trang web để thực hiện lấy dữ liệu
        data = []
        count = 0
        for bank in bank_list:
            for card_type in card_type_list:
                url = f'https://thebank.vn/the-tin-dung.html?id_bank={bank[0]}?type={card_type[0]}'
                self.driver.get(url)
                time.sleep(self.sleep_time)
                
                # Chạy sao cho ấn đến khi không còn xem thêm thì dừng
                while True:
                    try:
                        show_more_classname = r'show_more_card'
                        show_more = self.driver.find_element(By.CLASS_NAME, show_more_classname)
                        show_more.click()
                        time.sleep(1)
                    except Exception:
                        break
                
                # kéo xuống cuối trang
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                # lấy danh sách thẻ
                card_selector = r'.list_card_data'
                cards = self.driver.find_elements(By.CSS_SELECTOR, card_selector)
                MAX_VALUE = 10**18
                for card in cards:
                    try:
                        # lấy tên thẻ
                        card_name = card.find_element(By.CLASS_NAME, 'name_card').find_element(By.TAG_NAME, 'h3').text
                        #lấy hạn mức thẻ
                        card_limit = card.find_element(By.CLASS_NAME, 'hm_detail').text
                        card_limit = [self.process_money(txt.strip()) for txt in card_limit.split("-")]
                        income = re.findall('\d+',card.find_element(By.CLASS_NAME, 'in_detail').text)[0]
                        #lấy ảnh từ thẻ
                        img = card.find_element(By.CLASS_NAME, r'sp_detail').find_element(By.TAG_NAME, 'img')
                        img_src = img.get_attribute('src')
                        image_name = f"{count}.png"
                        count+=1
                        request.urlretrieve(img_src, os.path.join('.\image',image_name))
                        
                        # lưu dữ liệu và mảng data
                        new_data = [
                            bank[1], 
                            card_type[1], 
                            card_name, 
                            card_limit[0], 
                            card_limit[1] if len(card_limit)==2 else MAX_VALUE,
                            int(income) * 10**6,
                            image_name
                        ]
                        print("="*100)
                        print(new_data)
                        print("="*100)
                        
                        data.append(new_data)
                    except Exception:
                        pass
        
        # tạo DataFrame để lưu dữ liệu và lưu lại dưới dạng excel
        df = pd.DataFrame(data=data, columns=[
            'Bank name', 'Card type', 'Card name', 
            'Lower limit', 'Upper limit', 'Income', 
            'img_url'
        ])
        df.to_excel(self.save_path, engine='openpyxl', index=False)
        
        
if __name__ == "__main__":
    # Khởi tạo class
    crawler = BankCardCrawler()
    # Thực hiện láy dữ liệu
    crawler.do_crawl()