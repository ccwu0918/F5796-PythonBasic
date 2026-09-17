import requests as req
import threading
import time
from tqdm import tqdm

class Download:
    headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/605.1.15 (KHTML, like Gecko)'}
    
    def __init__(self, urls, max_download=4):
        self.max_download = max_download
        self.urls = urls

    def __download(self, url):
        filename = url.split('/')[-1]
        print(filename)
        r = req.get(url, stream=True)
        with open(filename, 'wb') as f:
            try:
                for data in tqdm(r.iter_content(1024)):
                    f.write(data)
            except:
                print('下載出錯啦！')

        print(f'{url}下載完畢！')

    def start(self):
        downloading = True   # 設定目前「正在下載」
        threads = []         # 儲存執行緒的列表
        url_index = 0        # 下載網址的索引編號

        group = self.urls[:self.max_download]  # 取出前幾個下載網址

        for url in group:
            # 設置執行緒並將它加入列表
            threads.append(threading.Thread(target=self.__download, args=(url,)))

        for t in threads:
            t.start()  # 啟動列表裡的執行緒

        # 紀錄下一個網址索引編號
        if len(self.urls) > self.max_download:
            url_index = self.max_download
        else:
            downloading = False  # 檔案全部下載完畢！

        while downloading:
            for t in threads:
                if not t.is_alive():
                    threads.remove(t)

                    if url_index < len(self.urls):
                        url = self.urls[url_index]
                        threads.append(threading.Thread(target=self.__download, 
                                                        args=(url,)))
                        threads[-1].start()
                        url_index += 1
                    else:
                        downloading = False # 檔案全部下載完畢！
