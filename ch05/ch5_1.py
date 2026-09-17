# 參閱5-4頁

import os

path = os.environ.get('PATH')
print('系統PATH：', path)

home = os.path.expanduser('~')
print('家目錄：', home)

pict_path = os.path.join(home, 'Pictures', '照片.jpg')
print('圖像路徑：', pict_path)
