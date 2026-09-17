# 參閱8-19頁

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()      
# 建立 Chrome 瀏覽器驅動物件 
driver.get('https://tw.yahoo.com/')

search_field = driver.find_element(By.XPATH, "//input[@name='p']")
search_field.send_keys('超圖解Python物聯網')
search_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
search_btn.click()