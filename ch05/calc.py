# 參閱5-23頁

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--sum', nargs='+', type=int,
                    required=True, help='計算加總', action='store')

args = parser.parse_args()
total = 0

print('sum參數列表：', args.sum)

for val in args.sum:
    total += val

print('加總結果：', total)
