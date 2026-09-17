# 參閱8-32頁

from selenium import webdriver
from urllib import parse
driver = webdriver.Chrome()
search_key=parse.quote('防災包')  # 經過 URL 編碼的商品關鍵字
url = (f"https://www.momoshop.com.tw/search/searchShop.jsp?"
       f"keyword={search_key}")
driver.get( url ) # 開啟指定頁