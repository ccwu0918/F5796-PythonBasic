import time

data = [4,9,16]

def calc_square(nums):  # 計算平方的函式
    for n in nums:
        time.sleep(0.5)
        print(f'{n}的平方是{n**2}')

def calc_root(nums):    # 計算平方根的函式
    for n in nums:
        time.sleep(0.5)
        print(f'{n}開根號是{n**0.5}')

start_time = time.time()
calc_square(data)
calc_root(data)
print('花費時間：', time.time()-start_time)
