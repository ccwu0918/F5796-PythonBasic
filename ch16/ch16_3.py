# 參閱16-13頁

from ultralytics import YOLO # 引用 YOLO 模組

model = YOLO("yolo12n.pt")   # 載入模型檔，建立「模型」物件
img_src = 'img/vehicles.jpg' # 僅讀取一張影像
model(img_src, save=True, show=True, classes=[1, 2, 3, 5, 6, 7])  # 執行偵測