# 參閱4-18頁

import math


def cirArea(r):
    '''
    計算圓面積
    參數 r：半徑值
    傳回值：圓面積
    '''
    area = math.pi * (r ** 2)
    return area


ans = cirArea(5)
print(ans)
