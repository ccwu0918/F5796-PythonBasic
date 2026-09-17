# 參閱15-30頁

import cv2
from pathlib import Path
import sys

# 模型檔的路徑
haar_file = Path(".") / "models" / "haar_face.xml"

try: # 嘗試載入哈爾特徵分類器
    face_haar = cv2.CascadeClassifier(haar_file)
except Exception as e:
    print(f"載入模型時發生錯誤: {e}")
    sys.exit(1)

if face_haar.empty():  # 檢查分類器是否成功載入
    print("出錯了～無法載入哈爾特徵分類器。")
    sys.exit(1)

cap = cv2.VideoCapture(0)  # 開啟攝影機

if not cap.isOpened():
    print("出錯了～無法開啟攝影機。")
    sys.exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # 轉為灰階影像
    faces = face_haar.detectMultiScale(gray, scaleFactor=1.2, 
                                       minNeighbors=6, minSize=(30, 30))
    for box in faces:
        # 在原始彩色影像上繪製藍色方框
        cv2.rectangle(frame, box, (255, 0, 0), 2)

    cv2.imshow("Face", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # 釋放攝影機資源
cv2.destroyAllWindows()