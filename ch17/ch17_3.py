# 參閱17-23頁

import cv2
from ultralytics import YOLO
from paddleocr import TextRecognition # 引用「文字識別」模組

model = YOLO('models/car_plate.pt')   # 載入預先訓練的車牌位置模型
img = 'img/ambulance.jpg'             # 汽車影像檔
results = model.predict(source=img, imgsz=640) # 使用 YOLO 偵測車牌
ocr = TextRecognition()    # 建立文字辨識的物件
car_img = cv2.imread(img)  # 使用 OpenCV 讀取影像

# 處理每個偵測到的物件
for r in results:
    for b in r.boxes:      # 擷取邊界框
        x1, y1, x2, y2 = map(int, b.xyxy[0])
        plate_img = car_img[y1:y2, x1:x2] # 擷取車牌區域
        # 在原始影像的車牌位置繪製邊框
        cv2.rectangle(car_img, (x1, y1), (x2, y2), (0, 255, 0), 1)
        # 用 PaddleOCR 辨識車牌 
        ocr_result = ocr.predict(plate_img)

        if ocr_result:     # 確認有偵測到車牌
            plate_text = ''.join([plate["rec_text"] for plate in ocr_result])
            print("車牌：", plate_text)
            cv2.putText(car_img, plate_text, (x1, y1 - 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, (0,255,0), 2)
        else:
            print("未偵測到車牌")

cv2.namedWindow("Car", cv2.WINDOW_NORMAL) # 自動調整視窗大小           
cv2.imshow('Car', car_img) # 顯示偵測結果影像
while cv2.getWindowProperty("Car", cv2.WND_PROP_VISIBLE) >= 1:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()  # 關閉所有 OpenCV 視窗