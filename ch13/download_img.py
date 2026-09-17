# 參閱13-10頁

import requests as req
from lxml import html
from tqdm import tqdm

# 偽裝成macOS系統的Safari瀏覽器
http_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko)'}

url = 'http://swf.com.tw/scrap/'
page = req.get(url, headers=http_headers)  # 設定HTTP標頭
dom = html.fromstring(page.text)
images = dom.xpath('//img/@src')


def download(url):
    filename = url.split('/')[-1]
    r = req.get(url, stream=True, headers=http_headers)  # 設定HTTP標頭

    with open(filename, 'wb') as f:
        for data in tqdm(r.iter_content(1024)):
            f.write(data)

    return filename


for img in images:
    if not img.startswith('http'):
        img = url + img

    h = req.head(img, headers=http_headers)  # 設定HTTP標頭
    MIME = h.headers['content-type']

    # 確認回應OK
    if (h.status_code == 200) and ('image' in MIME):
        print('下載檔案網址：' + img)
        filename = download(img)
        print(filename + ' 檔案下載完畢！')
