# 參閱8-32頁

titles = ['主機', '螢幕', '鍵盤']
prices = ['$9,999', '$2,999', '$399']

# for i in range(len(prices)):
#     print(titles[i] + '：' + prices[i])

# for i in range(len(prices)):
#     print(titles[i] + '：' + prices[i])

for t, p in zip(titles, prices):
    print(t + '：' + p)


products = [
 {'name':'貝雷帽', 'link':'hat.htm', 'price':520},
 {'name':'潮T', 'link':'shirt.htm', 'price':799},
 {'name':'人字拖', 'link':'slipper.htm', 'price':480}
]

print(products[2]['name'])