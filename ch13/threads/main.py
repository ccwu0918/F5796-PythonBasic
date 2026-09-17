from lxml import html
import requests as req
from thread_download import Download  # 引用自訂類別

url = 'http://swf.com.tw/download/'  # 包含下載檔案的網頁
page = req.get(url, headers=Download.headers)
dom = html.fromstring(page.text)
links = dom.xpath('//a/@href')
files = []   # 儲存下載檔案的列表

for href in links:
    if not href.startswith('http'):
        href = url + href

    h = req.head(href, headers=Download.headers)
    MIME = h.headers.get('content-type')

    if (h.status_code == 200) and ((MIME is None) or ('html' not in MIME)):
        print(href)
        files.append(href)  # 把檔案加入下載列表

dw = Download(files)   # 宣告「多執行緒下載」類別物件
dw.start()            # 開始下載列表裡的檔案