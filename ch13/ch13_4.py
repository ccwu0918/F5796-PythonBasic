# 參閱13-7頁

import requests as req
from tqdm import tqdm

url = 'http://swf.com.tw/scrap/img/IR.png'

# 偽裝成macOS系統的Safari瀏覽器
http_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko)'}


def download(url):
    filename = url.split('/')[-1]
    r = req.get(url, stream=True, headers=http_headers)  # 設定HTTP標頭

    # with open(filename, 'wb') as f:
    #     for data in r.iter_content(1024):
    #         f.write(data)

    with open(filename, 'wb') as f:
        for data in tqdm(r.iter_content(1024)):
            f.write(data)

    return filename


download(url)
