# 參閱13-25頁

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import time      # 新增引用此程式庫

url = 'https://swf.com.tw/download/dl_js.html'
driver = webdriver.Chrome()
driver.implicitly_wait(10)  # 隱性等待，最長 10 秒

driver.get(url)
links = driver.find_elements(By.XPATH, '//a')  # 取得所有超連結

file_set = set()  # 紀錄已下載檔案的集合
pattern = re.compile(r'[\w]+\.r(?:ar|\d{1,3})$')
for a in links:
    href = a.get_attribute("href")  # 取得超連結
    rar = pattern.search(href)

    if rar:
        filename = rar.group()       # 取出檔名
        if filename not in file_set: # 如果此檔案沒有下載過…
            a.click()                # 點擊此超連結（下載檔案）
            time.sleep(1)            # 暫停 1 秒鐘
            file_set.add(filename)   # 紀錄此檔案

driver.quit()  # 關閉瀏覽器
