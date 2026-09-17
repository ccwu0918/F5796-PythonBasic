# 參閱16-29頁

import cv2
from ultralytics import YOLO

model = YOLO("yolo12n.pt")

class CarCounter:
    def __init__(self, w, h, LV, LH):
        self.w = w   # 影片的寬度
        self.h = h   # 影片的高度
        self.line_v = LV    # 車道左右分離的位置
        self.line_h = LH     # 觸發計數車輛的位置
        self.right_counter = 0 # 右邊車道車輛的計數值
        self.left_counter = 0  # 左邊車道車輛的計數值
        self.uncount_right = {} # 紀錄右邊車道，尚未計數車輛的ID。
        self.uncount_left = {}  # 紀錄左邊車道，尚未計數車輛的ID。

    def update(self, id, box):
        x1, y1, x2, y2 = box  # 取得車輛的邊界框座標
        car_x = int(x1 + (x2 - x1) / 2) # 計算車輛的X軸中心點
        car_y = int(y1 + (y2 - y1) / 2) # 計算車輛的Y軸中心點

        # 檢查右邊車道(車輛從Y軸上到下移動)
        if car_x > self.line_v:
            # 如果車輛的ID不在「尚未計數」的字典中，而且…
            # 車體Y軸中心點位在水平中線上方，則加入字典。
            if id not in self.uncount_right and car_y < self.line_h:
                self.uncount_right[id] = car_y
            # 如果車輛的ID在「尚未計數」的字典中，而且…
            #  車體Y軸中心點越過水平中線，則計數+1並刪除字典中的ID
            elif id in self.uncount_right and car_y > self.line_h:
                self.right_counter += 1
                del self.uncount_right[id]

        # 檢查左邊車道 (車輛從Y軸下到上移動)
        elif car_x < self.line_v:
            if id not in self.uncount_left and car_y > self.line_h:
                self.uncount_left[id] = car_y
            elif id in self.uncount_left and car_y < self.line_h:
                self.left_counter += 1
                del self.uncount_left[id]

    def draw_counter(self, frame): # 顯示計數器
        cv2.line( # 畫紅色水平線
            frame, (0, self.line_h), (self.w, self.line_h), (0, 0, 255), 2
        )
        cv2.line( # 畫藍色垂直線
            frame, (self.line_v, 0), (self.line_v, self.h), (255, 0, 0), 2
        )
        cv2.putText( # 在左下角顯示左邊車道的計數
            frame, f"COUNT: {self.left_counter}", # 左計數值
            (30, self.h-50), # 文字的位置
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3 )
        cv2.putText(  # 在右下角顯示右邊車道的計數
            frame, f"COUNT: {self.right_counter}",
            (self.line_v + 30, self.h-50), # 文字的位置
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),3 )

def draw_label(frame, id, box):  # 顯示車輛的ID和邊界框
    COLORS = [
        (155, 80, 155),
        (155, 155, 255),
        (155, 200, 200),
        (200, 200, 200),
        (155, 255, 255),
        (255, 80, 0),
        (255, 80, 100),
        (255, 80, 255),
        (255, 120, 255),
        (255, 255, 0) ]

    color = COLORS[id % 10] # 依偵測物件的ID取色
    x1, y1, x2, y2 = map(int, box) 
    # 在汽車周圍繪製偵測框
    cv2.rectangle( frame, (x1, y1), (x2, y2), color, 2)
    # 在汽車上方顯示ID
    cv2.putText( frame, f"ID:{id}",  (x1, y1 - 15), 
              cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3 )

def main():
    cap = cv2.VideoCapture("videos/tokyo_720p.mp4")
    # 取得輸入影片的寬度、高度、FPS
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f"w:{w} h:{h} fps:{fps}")

    # 設定輸出影片的檔名、編碼格式、FPS和大小
    output_video = cv2.VideoWriter('car_counter.mp4',
                                 cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

    car_counter = CarCounter(w, h, int(w/2), int(h/2))

    while True:
        ret, frame = cap.read()
        if not ret:
            print("影片結束")
            break

        results = model.track(frame, persist=True, conf=0.3, classes=[2, 5, 7])
        for box in results[0].boxes:
            r = box.xyxy.tolist()
            id = int(box.id) if box.id is not None else 0
            car_counter.update(id, r[0])
            draw_label(frame, id, r[0])

        car_counter.draw_counter(frame)
        output_video.write(frame)
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    output_video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
