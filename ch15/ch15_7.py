# 參閱15-27頁

import cv2
import sys

cap = cv2.VideoCapture(0) # 捕捉預設攝影機的畫面

if not cap.isOpened():    # 加入此條件式判斷攝影機是否開啟
    print("出錯了～無法開啟攝影機。")
    sys.exit(1)           # 退出程式
        
print("攝影機已開啟。按下 'ESC' 鍵即可結束程式。")

while True:
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.flip(gray, 1)
    cv2.imshow('Webcam', gray)
    
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()