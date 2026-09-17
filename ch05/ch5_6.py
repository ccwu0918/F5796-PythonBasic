# 參閱5-13頁

import locale
import time

ticks = time.time()
print('現在時間：', ticks)

now = time.localtime(time.time())
print('本地時間：', now)

date_str = time.strftime('%Y/%m/%d', time.localtime())
print('本地日期：', date_str)

locale.setlocale(locale.LC_CTYPE, 'chinese')

date_str = time.strftime("%Y年%m月%d日", time.localtime())
print(date_str)
