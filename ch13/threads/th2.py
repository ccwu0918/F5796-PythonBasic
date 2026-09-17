import threading
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

start_time = time.time()  # 取得目前時間
t1 = threading.Thread(target=calc_square, args=(data,))
t2 = threading.Thread(target=calc_root, args=[data])
t1.start()
t2.start()
print('作用中的執行緒：', threading.active_count())
print('花費時間：', time.time()-start_time)
print('主程式執行完畢！')
