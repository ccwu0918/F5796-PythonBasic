# 參閱13-26頁

import time

data = [4,9,16]         # 計算資料
def calc_square(nums):  # 計算平方的函式
    for n in nums:
        time.sleep(0.5) # 暫停 0.5 秒
        print(f'{n}的平方是{n**2}')

def calc_root(nums):    # 計算平方根的函式
    for n in nums:
        time.sleep(0.5)
        print(f'{n}開根號是{n**0.5}')

start_time = time.time()  # 取得目前時間
calc_square(data)         # 計算平方
calc_root(data)           # 計算平方根
print('花費時間：', time.time()-start_time)