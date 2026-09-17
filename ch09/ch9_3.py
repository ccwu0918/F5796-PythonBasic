# 參閱9-15頁

import csv

with open('data.csv', 'r') as f:
    r = csv.reader(f, delimiter=',')

    for row in r:
        print(f'類型：{type(row)}，資料：{row}')
        # print(', '.join(row))
