# 參閱9-18頁

import csv
from datetime import datetime
import os

FETCH_LIMIT = 5   # 擷取資料筆數的上限，最多 5 筆
raw_key='防災包'   # 搜尋關鍵字

search_key=parse.quote(raw_key)   # 經過 URL 編碼的商品關鍵字
CSV_FILE_NAME = 'shop_data.csv'   # 儲存商品資料的 CSV

def save_to_csv(data, csv_file=CSV_FILE_NAME):
    # 定義 CSV 的標題
    csv_headers = ['日期時間', '商品名稱', '價格', '網址']  
    # 建立標題與原始資料鍵的對應關係
    key_mapping = {
        "日期時間": "date_time",
        "商品名稱": "name",
        "價格": "price",
        "網址": "url"
    }
    
    # 判斷檔案是否已存在，若不存在則建立新檔案
    file_exists = os.path.exists(csv_file)
    
    try:  # 寫入模式設為附加（a）
        with open(csv_file, 'a', newline='', 
                  encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, 
                                    fieldnames=csv_headers)
            if not file_exists:  # 若檔案不存在，則寫入標題列
                writer.writeheader()
            for d in data:
                row = {}  # 暫存轉換為符合 CSV 標題的一筆資料
                for header in csv_headers:
                    original_key = key_mapping.get(header)
                    row[header] = d.get(original_key)
                writer.writerow(row) # 寫入轉換 CSV 標題之後的資料
    except OSError as e: # 捕捉「系統錯誤」
        print(f"寫入檔案時出錯了；{e}")
    except Exception as e:
        print(f"發生未知錯誤：{e}")