# 參閱13-4頁

import requests as req

url = 'https://swf.com.tw/scrap'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.8,en-US,en;q=0.6"
}

resp = req.get(url, headers=headers)

print(resp.status_code)
print(resp.headers)
print(resp.headers['Content-Type'])
print(resp.content)

out = resp.content.decode('utf-8')
print(out)