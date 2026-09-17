# 參閱8-13頁

from selenium import webdriver
from selenium.webdriver.common.by import By  # 必須引用 By

driver = webdriver.Chrome()
driver.get('https://tw.yahoo.com')

search_field = driver.find_element(By.NAME, 'p')
search_field.send_keys('台灣矮黑人')
search_field.submit()   # 送出表單

# driver.back()
# search_field = driver.find_element(By.NAME, 'p')
# search_field.send_keys('時間旅行')

# from selenium.webdriver.common.keys import Keys
# search_field.send_keys(Keys.ENTER)

# body = driver.find_element(By.TAG_NAME, 'body')
# body.send_keys(Keys.PAGE_DOWN)