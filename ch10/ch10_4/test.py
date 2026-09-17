from model import sheet
from datetime import datetime

gs = sheet.GoogleSheet('谷歌試算表') # 開啟試算表

def main():
    print('標題列：', gs.headers)

    # if (len(gs.labels) == 0):
    #     gs.append_row(['日期時間', '商品標題', '價格', '網址'])

    dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    gs.resize()
    gs.append_row([dt, '毛線編織器', 399, 'swf.com.tw'])

if __name__ == "__main__":
    main()