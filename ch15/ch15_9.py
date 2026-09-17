# 參閱15-43頁

import cv2
import sys
from pathlib import Path

# YuNet 模型檔案的路徑
detector_model = Path("./models") / "face_detection.onnx"

try:
    face_detector = cv2.FaceDetectorYN.create(
        model=detector_model,
        config="",
        input_size=(320, 320),
        score_threshold=0.5,
        nms_threshold=0.3,
        top_k=5000
    )
except Exception as e:
    print(f"載入 YuNet 模型時發生錯誤: {e}")
    sys.exit(1)

cap = cv2.VideoCapture(0)  # 開啟攝影機

# 選擇性地設定攝影機的解析度
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 輸入影像的寬度設為 640
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) # 輸入影像的高度設為 480
# 此行可取代 try..except
assert cap.isOpened(), "出錯了～無法開啟攝影機。" 
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   
# 取得影格寬度
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 取得影格高度
fps = int(cap.get(cv2.CAP_PROP_FPS))         
# 取得 FPS
print(f"Webcam解析度，寬：{w} 高：{h} fps：{fps}")
# 設定攝影機的解析度程式結束

if not cap.isOpened():
    print("出錯了～無法開啟攝影機。")
    sys.exit(1)

print("攝影機已開啟。按下 'q' 鍵即可結束程式。")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape  # 獲取影像的尺寸
    face_detector.setInputSize((w, h)) # 設定輸入尺寸

    _, faces = face_detector.detect(frame)   # 偵測人臉
    # 若faces為None，則存入空列表（[]）
    faces = faces if faces is not None else []

    for face in faces:  # 遍覽偵測結果並繪製
        box = list(map(int, face[:4])) # 取得人臉邊界框
        cv2.rectangle(frame, box, (0, 255, 0), 2) # 繪製邊界框
        landmarks = list(map(int, face[4:14])) # 取得關鍵點
        for i in range(5):  # 繪製關鍵點標記
            cv2.circle(frame, (landmarks[i*2], landmarks[i*2+1]), 
                       2, (0, 0, 255), -1)
        confidence = face[14] # 取得置信度
        # 在邊界框上方顯示置信度
        cv2.putText(frame, f"{confidence:.2f}", (box[0], box[1] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Face Detection", frame)  # 顯示偵測畫面
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # 釋放資源
cv2.destroyAllWindows()