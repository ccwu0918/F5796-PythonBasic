# 參閱5-15頁

import os
import time

mt_sec = os.path.getmtime('照片.jpg')  # 請自行修改檔名
mt = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(mt_sec))
print('檔案修改時間：', mt)
