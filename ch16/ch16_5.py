# 參閱16-18頁

import cv2
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import numpy as np

model = YOLO("yolo12n.pt")              # 建立 YOLO 模型物件
image = cv2.imread('img/vehicles.jpg')  # 讀取影像

# 物件的中文譯名
coco_names = ["人", "腳踏車", "汽車", "機車", "飛機", "巴士", "火車",
 "卡車", "船", "交通號誌", "消防栓", "停止標誌", "停車計時器", 
"長椅", "鳥", "貓", "狗", "馬", "羊", "牛", "大象", "熊", "斑馬", 
"長頸鹿", "背包", "雨傘", "手提包", "領帶", "行李箱", "飛盤", 
"滑雪板", "滑雪板", "運動球", "風箏", "棒球棒", "棒球手套", "滑板", 
"衝浪板", "網球拍", "瓶子", "酒杯", "杯子", "叉","刀", "湯匙", "碗", 
"香蕉", "蘋果", "三明治", "柳橙", "花椰菜", "胡蘿蔔", "熱狗", "披薩", 
"甜甜圈", "蛋糕", "椅子", "沙發", "盆栽", "床", "餐桌", "馬桶", 
"電視螢幕", "筆記型電腦", "滑鼠", "遙控器","鍵盤", "手機", "微波爐", 
"烤箱", "烤麵包機", "水槽", "冰箱", "書", "時鐘", "花瓶","剪刀", 
"泰迪熊", "吹風機", "牙刷"]

# 限定偵測：腳踏車(1), 汽車(2), 機車(3), 巴士(5), 火車(6), 卡車(7)
results = model(image, classes=[1, 2, 3, 5, 6, 7], conf=0.4)
for result in results:
    boxes = result.boxes
    for b in boxes:
        # 取得辨識邊界框的左上右下座標
        x1, y1, x2, y2 = b.xyxy[0]
        # 轉成整數
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) 
        coco_idx = int(b.cls[0])  # 取得辨識物件的分類碼
        name = coco_names[coco_idx] # 依分類碼取得中文名稱
        # 置信度，取至小數點後兩位
        conf = round(b.conf[0].item(), 2) 
        label = name + ":" + str(conf)
        # 使用 PIL 繪製框線和文字
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        # 思源黑體字
        font = ImageFont.truetype("SourceHanSansTC-VF.ttf", 20)
        # 繪製矩形框，外框為橙色
        draw.rectangle([x1, y1, x2, y2], outline='orange', width=2)
        # 取得文字的寬度和高度
        _, _, txt_w, txt_h = draw.textbbox((0, 0), label, font=font)

        top = (x1, y1-txt_h-4)    # 左上座標
        bottom = (x1+txt_w+4, y1)  # 右下座標
        draw.rectangle([top, bottom], fill='orange') # 橙色矩形
        draw.text((x1+2, y1-txt_h-2), label, font=font, fill='black')   # 填入黑色字
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

cv2.imshow("Photo", image)  # 設定名為 "Photo" 的視窗，顯示影像
while cv2.getWindowProperty("Photo", cv2.WND_PROP_VISIBLE) >= 1:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break