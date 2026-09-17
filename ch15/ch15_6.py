# 參閱15-25頁

import cv2

from pathlib import Path
path_obj = Path('./img') / 'arch.jpg'
img = cv2.imread(str(path_obj))        
# 讀取影像
if img is None:  # 檢查圖片是否成功讀取
    print(f"讀取 '{ str(path_obj) }' 影像時出現錯誤。")
else:
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 轉成灰階
    cv2.imshow('Original', img)        # 顯示原始影像
    cv2.imshow('Grayscale', gray_img)  # 顯示灰階影像
    print("按任意鍵即可關閉所有視窗")
    cv2.waitKey(0)          #  等待使用者按下任意鍵
    cv2.destroyAllWindows() # 關閉 OpenCV 建立的全部視窗