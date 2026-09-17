# 參閱8-20頁

from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()            
# 建立瀏覽器驅動物件 
driver.get('https://swf.com.tw/scrap') # 要擷取的網頁
h2 = driver.find_element(By.XPATH, "//div[@id='article1']/h2")
print('文章標題：', h2.text)  # 文章標題

# a_tag = driver.find_element(By.XPATH, "//div[@id='article1']//a")
# a_tag.get_attribute('href')  # 傳回 'http://swf.com.tw/?p=179'

# h1 = driver.find_element(By.XPATH, "//div[@id='header']/h1")
# print(h1.text)    # 顯示：手作×DIY

# h1 = driver.find_element(By.XPATH, "//div[@id='header']/h1")
# print(h1.get_attribute('innerHTML'))