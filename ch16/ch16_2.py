# 參閱16-12頁

from ultralytics import YOLO # 引用 YOLO 模組

model = YOLO("yolo12n.pt")   # 載入預訓練模型，建立模型物件
img_src = ['img/vehicles.jpg', 'img/train.jpg']          # 設定影像檔路徑檔名
model.predict(img_src, conf=0.25, save=True, show=True)  # 偵測影像
# model(img_src, conf=0.25, save=True, show=True)        # 偵測影像