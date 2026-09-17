# 參閱9-16頁

import csv

with open('data2.csv', 'r', encoding='utf-8') as f:
    r = csv.DictReader(f)
    
    for row in r:
        print(row['商品標題'], row['價格'])