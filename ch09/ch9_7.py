# 參閱9-16頁

import csv

with open('data2.csv', 'w', newline='',   ) as f:
    headers = ['商品標題', '價格']
    w = csv.DictWriter(f, fieldnames=headers)
    
    w.writeheader()
    w.writerow({'商品標題': '空氣清靜機', '價格': '$3,980'})
    w.writerow({'商品標題': '掃地機器人', '價格': '$7,980'})