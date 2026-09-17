# 參閱16-46頁

import cv2
import math
from ultralytics import YOLO

UP_THRESHOLD = 150    # 手臂平放時的角度
DOWN_THRESHOLD = 90   # 手臂彎曲時的角度
WIDTH = 1280          # 視訊畫面寬度
HEIGHT = 720          # 視訊畫面高度
right_is_down = False # 右手臂是否平放，預設為否。
right_counter = 0     # 右手臂計數器
left_is_down = False  # 左手臂是否平放，預設為否。
left_counter = 0      # 左手臂計數器
FONT = cv2.FONT_HERSHEY_SIMPLEX  # 字體

def calc_angle(s, e, w):  # 肩、肘、腕三點座標
    se = (s[0] - e[0], s[1] - e[1])  # 座標點轉換成向量（肩→肘）
    we = (w[0] - e[0], w[1] - e[1])  # 「腕→肘」向量
    
    dot_product = se[0] * we[0] + se[1] * we[1]  # 計算向量的點積
    mag1 = math.sqrt(se[0]**2 + se[1]**2)        # 肩→肘的向量長度
    mag2 = math.sqrt(we[0]**2 + we[1]**2)        # 腕→肘的向量長度

    if mag1 * mag2 == 0: # 避免除以0的錯誤
        return 180

    angle_rad = math.acos(dot_product / (mag1 * mag2))  # 夾角的弧度
    angle_deg = math.degrees(angle_rad)  # 弧度轉角度
    
    return angle_deg

def draw_circle_label(frame, keypoint, point_id):
    """在影格上繪製關節點圓圈與其編號"""
    x, y = int(keypoint[0]), int(keypoint[1])
    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # 綠色圓點
    cv2.putText(frame, str(point_id), (x + 5, y - 5), FONT, 0.5, (255, 0, 0), 2) # 藍色編號

def check_arm(frame, person, arm_idx, is_down, counter, pos):
    """
    處理單邊手臂的彎舉計數邏輯。

    參數：
        frame: 要繪製的影像畫面
        person: 單一人物的所有關節點座標
        arm_idx: 對應手臂的肩、肘、腕關節點索引。
        is_down: 目前手臂處於平放 (True) 還是彎曲 (False) 狀態
        counter: 計數值
        pos: 在畫面上顯示計數文字的位置 (x, y)。

    傳回值：
        更新後的 (is_down, counter) 元組
    """
    shoulder = person[arm_idx[0]]  # 提取肩部關節點座標
    elbow = person[arm_idx[1]]     # 提取肘部關節點座標
    wrist = person[arm_idx[2]]     # 提取腕部關節點座標

    # 確保三個關節點都被偵測到 (座標不為0)
    if shoulder[0] > 0 and elbow[0] > 0 and wrist[0] > 0:
        # 計算手肘角度
        angle = calc_angle(shoulder, elbow, wrist)
        
        # 顯示角度值
        cv2.putText(frame, f'{int(angle)}', (pos[0], pos[1]+50), FONT, 1, (255, 255, 255), 2)

        # 手臂彎曲 <= 90度，且目前狀態不是「平放」…
        if angle <= DOWN_THRESHOLD and not is_down:
            is_down = True  # 手臂進入「平放」狀態
        # 手臂平放 >= 150度，且目前狀態是「平放」…
        elif angle >= UP_THRESHOLD and is_down:
            counter += 1     # 計數器加1
            is_down = False  # 手臂進入「舉起」狀態
            
    # 在指定位置顯示計數值
    cv2.putText(frame, f'{counter}', pos, FONT, 3, (0, 0, 255), 5)
    
    return is_down, counter

model = YOLO('yolo11n-pose.pt')  # 載入姿態估算模型

cap = cv2.VideoCapture(0) # 開啟鏡頭

if not cap.isOpened():
    print("錯誤：無法開啟視訊檔案或鏡頭。")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("視訊結束或讀取錯誤。")
        break
    
    frame = cv2.resize(frame, (WIDTH, HEIGHT))  # 調整畫面大小

    # 追蹤人體姿態，persist=True 代表在連續影格間保持追蹤。
    results = model.track(frame, persist=True)
    
    # 檢查是否有偵測到人
    if results[0].keypoints is not None:
        # 獲取所有偵測到的關節點
        kp_data = results[0].keypoints.xy.cpu().numpy()
        
        for person in kp_data:    # 遍覽每個被偵測到的人
            right_is_down, right_counter = check_arm(
                frame, person,
                arm_idx=(6, 8, 10),    # 右手臂關節點索引
                is_down=right_is_down, # 手臂平放或舉起狀態
                counter=right_counter, # 右手臂計數值
                pos=(50, 100)          # 計數值顯示座標
            )
            
            left_is_down, left_counter = check_arm(
                frame, person,
                arm_idx=(5, 7, 9),     # 左手臂關節點索引
                is_down=left_is_down,  # 手臂平放或舉起狀態
                counter=left_counter,  # 左手臂計數值
                pos=(WIDTH - 150, 100) # 計數值顯示座標
            )

            for i in range(5, 11):   # 遍覽手臂關節點 (5到10)
                if person[i][0] > 0: # 僅在偵測到時繪製
                    draw_circle_label(frame, person[i], i)

    cv2.imshow("Dumbbell", frame)  # 顯示結果畫面
    
    key = cv2.waitKey(1) & 0xFF    # 按'q'或'Esc'鍵退出
    if key == ord('q') or key == 27:
        break

cap.release()  # 釋放資源
cv2.destroyAllWindows()