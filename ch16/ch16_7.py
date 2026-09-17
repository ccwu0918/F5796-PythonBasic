# 參閱16-23頁

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time
from ultralytics import YOLO

cap = cv2.VideoCapture("videos/cars.mp4")
assert cap.isOpened(), "影片檔讀取失敗！"  # 用assert取代條件式
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 影片寬
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 影片高
fps = int(cap.get(cv2.CAP_PROP_FPS)) # 來源影片的FPS

print(f"影片寬：{w}、高：{h}、fps:{fps}")
output_video = cv2.VideoWriter('output.mp4', 
               cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

model = YOLO("yolo12n.pt") # 下載yolo12n.pt模型

coco_names = ["人", "腳踏車", "汽車", "機車", "飛機", "巴士", "火車", "卡車", "船", 
"交通號誌", "消防栓", "停止標誌", "停車計時器", "長椅", "鳥", "貓", "狗",
"馬", "羊", "牛", "大象", "熊", "斑馬", "長頸鹿", "背包", "雨傘",
"手提包", "領帶", "行李箱", "飛盤", "滑雪板", "滑雪板", "運動球", "風箏", 
"棒球棒", "棒球手套", "滑板", "衝浪板", "網球拍", "瓶子",
"酒杯", "杯子", "叉", "刀", "湯匙", "碗", "香蕉", "蘋果", "三明治", "柳橙",
"花椰菜", "胡蘿蔔", "熱狗", "披薩", "甜甜圈", "蛋糕", "椅子", "沙發", "盆栽", "床", 
"餐桌", "馬桶", "電視螢幕", "筆記型電腦", "滑鼠", "遙控器", "鍵盤", "手機", 
"微波爐", "烤箱", "烤麵包機", "水槽", "冰箱", "書", "時鐘", "花瓶", "剪刀", 
"泰迪熊", "吹風機", "牙刷"
]
ctime = 0  # 當前時間
ptime = 0  # 上次更新時間
while True:
    ret, frame_cv2 = cap.read()
    if ret:
        # 僅偵測2汽車、5巴士、7卡車
        results = model(frame_cv2, conf=0.35, iou = 0.1, classes=[2, 5, 7])
        # 把OpenCV的影格轉成PIL的影像
        frame_pil = Image.fromarray(cv2.cvtColor(frame_cv2, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(frame_pil)
        font = ImageFont.truetype("SourceHanSansTC-VF.ttf", 20)  # 思源黑體

        for r in results:
            boxes = r.boxes
            for b in boxes:
                x1, y1, x2, y2 = map(int, b.xyxy[0]) # 取得邊界框的座標
                # 依邊界框座標，繪製橙色、2像素粗細的矩形框
                draw.rectangle([x1, y1, x2, y2], outline="orange", width=2)
                name = coco_names[int(b.cls[0])]  # 取得物件名稱
                conf = round(b.conf[0].item(), 2) # 置信度取到小數點後兩位
                label = f"{name}: {conf}"
                # 取得文字的寬度和高度
                _, _, txt_w, txt_h = draw.textbbox((0, 0), label, font=font)
                top = (x1-2, y1-txt_h-4)   # 左上座標
                bottom = (x1+txt_w+4, y1+2) # 右下座標
                draw.rectangle([top, bottom], fill='orange') # 橙色矩形背景
                draw.text((x1+1, y1-txt_h-1), label, font=font, fill='black')

        # 將PIL影像轉回OpenCV格式
        frame_output = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)

        ctime = time.time()       # 取得當前時間
        fps = 1 / (ctime - ptime) # 計算FPS
        ptime = ctime  # 更新上次時間
        cv2.putText(frame_output, f"FPS: {int(fps)}", (30, 680), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        output_video.write(frame_output)  # 將影格畫面存入輸出影片
        cv2.imshow("Video", frame_output) # 顯示影格畫面

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
    
cap.release()
output_video.release()   # 釋放影片物件
cv2.destroyAllWindows()  # 關閉所有OpenCV視窗