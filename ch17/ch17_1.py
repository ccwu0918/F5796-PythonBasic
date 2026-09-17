# 參閱17-20頁

from ultralytics import YOLO

model = YOLO('models/car_plate.pt')  # 載入偵測車牌的模型

results = model.predict(source='img/ambulance.jpg', imgsz=640)
for result in results:
    result.show()    # 顯示偵測到的車牌