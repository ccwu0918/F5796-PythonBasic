# 參閱5-7頁

import shutil

total, used, free = shutil.disk_usage('.')

gb = 2 ** 30

print('磁碟容量：{:.2f} GB'.format(total / gb))
print('已使用空間：{:.2f} GB'.format(used / gb))
print('可用空間：{:.2f} GB'.format(free / gb))
