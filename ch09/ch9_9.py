# 參閱9-29頁

import gspread

client = gspread.service_account(filename="service_account.json")
sh = client.open('谷歌試算表') # 開啟試算表，傳回「試算表物件」
wks = sh.sheet1               # 存取「工作表1」，傳回「工作表物件」
# wks = sh.worksheet('網購商品')

wks.update_acell('D2', 'swf.com.tw')
# wks.update_cell(2, 4, 'swf.com.tw')

headers = ['日期時間', '商品標題', '價格', '網址']
wks.insert_row(headers, 1)