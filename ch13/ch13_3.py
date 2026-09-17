# 參閱13-6頁

import requests as req

url = 'http://swf.com.tw/scrap/img/IR.png'
file_name = url.split('/')[-1]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.8,en-US,en;q=0.6"
}

resp = req.get(url, headers=headers)

with open(file_name, 'wb') as f:
    f.write(resp.content)