# 參閱13-14頁

from lxml import html
from tqdm import tqdm
import requests as req

# 偽裝成macOS系統的Safari瀏覽器
http_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko)'}

url = 'http://swf.com.tw/download/'
page = req.get(url, headers=http_headers)  # 設定HTTP標頭
dom = html.fromstring(page.text)
links = dom.xpath('//a/@href')


def download(url):
    filename = url.split('/')[-1]
    r = req.get(url, stream=True, headers=http_headers)  # 設定HTTP標頭

    with open(filename, 'wb') as f:
        for data in tqdm(r.iter_content(1024)):
            f.write(data)

    return filename


for href in links:
    if not href.startswith('http'):
        href = url+href
    h = req.head(href, headers=http_headers)  # 設定HTTP標頭
    MIME = h.headers.get('content-type')

    if (h.status_code == 200) and \
            ((MIME is None) or ('html' not in MIME)):
        print('下載檔案網址：' + href)
        filename = download(href)
        print(filename + ' 下載完畢！')
