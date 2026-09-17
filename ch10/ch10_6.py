# 參閱10-25頁

import pickle

data = [
    {
        '網站': 'https://tw.bid.yahoo.com/',
        '標題': ['神臂鬥士 arms', 'Switch 神臂鬥士 arms ns 任天堂'],
        '價格':['$1150', '$1300']
    },
    {
        '網站': 'https://shopee.tw/',
        '標題': ['任天堂Switch遊戲，ARMS 神臂鬥士', 'ARMS 神臂鬥士~可面交'],
        '價格':['$1,300', '$1,400']
    }
]

with open('arms.dat', 'wb') as f:
    pickle.dump(data, f)
