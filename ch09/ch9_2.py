# 參閱9-13頁

import csv

titles = ['主機', '螢幕', '鍵盤']
prices = ['$9,999', '$2,999', '$399']

with open('data.csv', 'w', newline='') as f:
    w = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    w.writerow(['商品標題', '價格'])

    for t, p in zip(titles, prices):
        w.writerow([t, p])
