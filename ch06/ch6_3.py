# 參閱6-21頁

import time
i = 0
try:
    while True:
        i += 1
        print('\r計數：{}'.format(i), end = '\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    print('結束計數，i=', i)