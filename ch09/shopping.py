
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from urllib import parse
import csv
from datetime import datetime
import os
from model import sheet  # 載入自訂的google試算表模組

FETCH_LIMIT = 5 # 擷取資料筆數的上限，最多5筆
raw_key='防災包'  # 搜尋關鍵字
search_key=parse.quote(raw_key)   # 經過URL編碼的商品關鍵字
CSV_FILE_NAME = 'shop_data.csv'  # 儲存商品資料的CSV

sites=[  # 各個網站的連結和XPath
    {
        "company":'MOMO購物網',
        "url":'https://www.momoshop.com.tw/search/'
              'searchShop.jsp?keyword={key}',
        "root_path":'//ul[@class="listAreaUl"]/li[@class="listAreaLi"]',
        "price_path":'.//span[@class="price"]',
        "link_path":'.//a[@href]'
    },
    {
        "company":'家樂福線上購物',
        "url":'https://online.carrefour.com.tw/zh/search/?q={key}',
        "root_path":'//div[@id="productgrid"]/div[@class="hot-recommend-item line"]',
        "price_path":'.//div[@class="commodity-operation"]//div[@class="current-price"]',
        "link_path":'.//div[@class="commodity-desc"]//a'
    }
]

products_data = [] # 儲存商品資料的列表

chrome_options = Options()

# 將各種設定參數加入「選項設置」物件中
chrome_options.add_argument("--headless") # 啟用「無頭」模式
chrome_options.add_argument("--disable-gpu") # 停用GPU
chrome_options.add_argument("--window-size=1920,1080") # 設定視窗大小
chrome_options.add_argument("--ignore-certificate-errors") # 忽略憑證錯誤
driver = webdriver.Chrome(options=chrome_options)

# 接收網站名稱、網址、商品列表的根Xpath、價格XPath及超連結XPath
def open_page(company, url, root_path ,price_path, link_path):
    driver.get(url) # 開啟指定頁面

    WebDriverWait(driver, 15).until(  # 確保商品頁面已經載入
        EC.presence_of_element_located((By.XPATH, root_path))
    )

    shop_items = driver.find_elements(By.XPATH, root_path)
    total_items = len(shop_items)
    print(f"\n在「{company}」找到 {total_items} 項商品。")
    max_items = min(total_items, FETCH_LIMIT)  # 最多擷取FETCH_LIMIT筆資料

    for i, item in enumerate(shop_items[:max_items]):
        print(f"\n--- 處理第 {i+1} 項商品 ---")
        product_info = {
            "date_time": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),  # 當前日期時間
            "name": None,      # 商品名稱
            "price": None,     # 商品價格
            "link": None       # 商品連結
        }
        item_found = False

        try:
            link_el = item.find_element(By.XPATH, link_path)
            product_info["name"] = link_el.get_attribute('title')
            print(f"  品名：{product_info['name']}")
            product_info["link"] = link_el.get_attribute('href')
            print(f"  商品連結：{product_info['link']}")

            # 取得商品價格，使用相對路徑查找，確保只在當前item內。
            price_el = item.find_element(By.XPATH, price_path)
            raw_price = price_el.text.strip()
            product_info["price"] = raw_price.replace('$', '').replace(',', '')
            # product_info["price"] = price_el.text.strip()
            print(f"  價格：{product_info['price']}")

            item_found = True

        except Exception as e:
            print(f"處理這項商品時出錯了：{e}")

        if item_found:
            products_data.append(product_info)
        else:
            print(f"提取商品過程出現錯誤，因而跳過 {i+1} 項。")

def save_to_google(data, file_name, wks_title):
    gs = sheet.GoogleSheet(file_name, wks_title)  # 建立Google試算表物件
    gs.resize()  # 調整工作表大小

    for d in data:  # 把字典資料轉換為列表格式
        row = [
            d.get("date_time", ""),
            d.get("name", ""),
            d.get("price", ""),
            d.get("link", "")
        ]
        gs.append_row(row) # 新增一筆資料

def save_to_csv(data, csv_file=CSV_FILE_NAME):
    # 定義CSV檔案的標題
    csv_headers = ['日期時間', '商品名稱', '價格', '網址']

    # 建立標題與原始資料鍵的對應關係
    key_mapping = {
        "日期時間": "date_time",
        "商品名稱": "name",
        "價格": "price",
        "網址": "link"
    }

    # 判斷檔案是否已存在，若不存在則建立新檔案
    file_exists = os.path.exists(csv_file)
    write_mode = 'a' if file_exists else 'w'

    try:
        with open(csv_file, write_mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)

            # 若檔案不存在，則寫入標題列
            if not file_exists:
                writer.writeheader()

            for d in data:
                row = {}  # 暫存轉換為符合CSV標題的一筆資料
                for header in csv_headers:
                    original_key = key_mapping.get(header)
                    if original_key:
                        # 若原始鍵不存在則預設為空字串
                        row[header] = d.get(original_key, "")
                    else:
                        # 如果標題沒有對應的原始鍵，則留空
                        row[header] = ""

                writer.writerow(row)

    except IOError:
        print(f"I/O錯誤：無法寫入{csv_file}")
    except Exception as e:
        print(f"發生未知錯誤：{e}")

if __name__ == "__main__":
    for s in sites:  # 從sites列表，逐一取得每個網站的網址和XPath
        company = s['company']  # 網站名稱
        url = s['url'].format(key=search_key) # 網址，填入關鍵字
        root_path = s['root_path']      # 商品列表的根Xpath
        price_path = s['price_path']    # 價格XPath
        link_path = s['link_path']      # 商品連結XPath

        open_page(company, url, root_path, price_path, link_path)

    if products_data:
        save_to_csv(products_data)  # 儲存資料到CSV檔案
        print(f"\n商品資料已儲存到 {CSV_FILE_NAME}。")
        # 儲存到Google試算表
        # save_to_google(products_data, '谷歌試算表', '網購商品')
        # print("\n商品資料已儲存到Google試算表。")
    else:
        print("\n沒有取得任何商品資料。")


    driver.quit()   # 關閉瀏覽器，釋放資源。
    print("瀏覽器已關閉。")