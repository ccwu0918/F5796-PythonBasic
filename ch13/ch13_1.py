# 參閱13-3頁

import requests as req    # 習慣上將requests設成req別名
url = 'https://swf.com.tw/scrap'
resp = req.get(url)       # 發起GET請求

print(resp.status_code)   # 查看狀態碼
print(resp.reason)        # 查看原因