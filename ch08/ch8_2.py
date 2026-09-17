# 參閱8-18頁

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()                  # 建立Chrome瀏覽器驅動物件
url = 'https://swf.com.tw/scrap/simple.html' # 要擷取的網頁位址
driver.get(url)
h1 = driver.find_element(By.XPATH, '//h1')
print('標題文字：', h1.text)
driver.quit()
