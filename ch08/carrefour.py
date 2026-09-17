from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
url = "https://online.carrefour.com.tw/zh/search/?q=防災包"
driver.get(url) # 開啟指定頁面

try:
    # 等待UL標記出現，確保商品頁面已經載入
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//div[@id="productgrid"]'))
    )

    # 找出全部商品項目（<li>元素）
    shop_items = driver.find_elements(By.XPATH, '//div[@id="productgrid"]/div[@class="hot-recommend-item line"]')

    products_data = [] # 儲存商品資料的列表

    print(f"找到 {len(shop_items)} 項商品。")

    # 取得每個商品的資料：名稱、價格、連結和圖片網址。
    for i, item in enumerate(shop_items):
        product_info = {
            "name": None,      # 商品名稱
            "price": None,     # 商品價格
            "link": None       # 商品連結
        }
        item_found = False # 標記是否成功找到商品資料的布林值

        print(f"\n--- 處理第 {i+1} 項商品 ---")

        try:
            # 取得商品名稱，使用相對路徑查找，確保只在當前item內。
            # 使用h3標籤和class名稱來定位商品名稱元素
            link_element = item.find_element(By.XPATH, './/div[@class="commodity-desc"]//a')
            product_info["name"] = link_element.text.strip()
            print(f"  品名：{product_info['name']}")
            product_info["link"] = link_element.get_attribute('href')
            print(f"  商品連結：{product_info['link']}")

            # 取得商品價格，使用相對路徑查找，確保只在當前item內。
            # 使用span標籤和class名稱來定位價格元素
            price_element = item.find_element(By.XPATH, './/div[@class="commodity-operation"]//div[@class="current-price"]')
            product_info["price"] = price_element.text.strip()
            print(f"  價格：{product_info['price']}")

            item_found = True

        except Exception as e:
            print(f"處理這項商品時出錯了：{e}")

        if item_found:
            products_data.append(product_info)
        else:
            print(f"提取商品過程出現錯誤，因而跳過 {i+1} 項。")


    print(f"\n--- 商品資料擷取完成 ---")
    print(f"成功取得 {len(products_data)} 項商品資料。")

except Exception as e:
    print(f"在網頁上找不到指定的UL標籤元素，或發生其他錯誤：{e}")

finally:
    driver.quit()   # 關閉瀏覽器，釋放資源。
    print("瀏覽器已關閉。")