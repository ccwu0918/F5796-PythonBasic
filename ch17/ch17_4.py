# 參閱17-25頁

import cv2
from ultralytics import YOLO
from paddleocr import PaddleOCR
from PIL import Image
import re

model = YOLO('models/car_plate.pt')     # 載入自行訓練的模型
car_image = 'img/ambulance.jpg'         # 載入包含車牌的汽車影像

valid_patterns = [          # 定義有效的車牌格式
    r'^[A-Z]{3}-\d{4}$',    # ▢▢▢-◯◯◯◯
    r'^[A-Z0-9]{2}-\d{4}$', # △△-◯◯◯◯
    r'^\d{4}-[A-Z0-9]{2}$', # ◯◯◯◯-△△
    r'^[A-Z0-9]{2}-\d{3}$', # △△-◯◯◯
    r'^\d{3}-[A-Z0-9]{2}$'  # ◯◯◯-△△
]

# 定義相似的字母和數字之間的對應關係
corrections = {
    'O': '0', '0':'O', 
    'I': '1', '1': 'I', '|':'1', 
    'Z': '2', '2': 'Z',
    'S':'5', '5':'S',
    'B': '8', '8': 'B'
}

def correct_plate_text(plate_text):
    """修正潛在OCR的解讀錯誤，同時確保車牌格式是正確的。"""
    if '-' in plate_text:
        prefix, suffix = plate_text.split('-')

        # 若「前綴」是3個字母，而任一字元是數字，則更正為字母。
        if len(prefix) == 3 and any(char.isdigit() for char in prefix):
            prefix = ''.join(
                corrections.get(char, char) if char.isdigit() else char
                for char in prefix
            )

        # 若「前綴」是4個數字，而任一字元是字母，則更正為數字。
        elif len(prefix) == 4 and any(char.isalpha() for char in prefix):
            prefix = ''.join(
                corrections.get(char, char) if char.isalpha() else char
                for char in prefix
            )

        # 若「後綴」是4個數字，而任一字元是字母，則更正為數字。
        if len(suffix) == 4 and any(char.isalpha() for char in suffix):
            suffix = ''.join(
                corrections.get(char, char) if char.isalpha() else char
                for char in suffix
            )

        # 驗證更正後的格式
        corrected_text = f"{prefix}-{suffix}"
        if any(re.match(pattern, corrected_text) for pattern in valid_patterns):
            return corrected_text
        else:
            print(f"車牌格式錯誤：{corrected_text}")

    return plate_text

# 偵測影像中的車牌
results = model.predict(source=car_image, imgsz=640)

# 使用英文語言模型和角度分類器初始化PaddleOCR
ocr = PaddleOCR(lang='en', use_angle_cls=True)

# 處理每個偵測到的車牌
for result in results:
    # 把影像從OpenCV格式轉換為PIL格式
    pil_image = Image.fromarray(cv2.cvtColor(result.orig_img, cv2.COLOR_BGR2RGB))
    pil_image.show()

    # 擷取邊界框並裁切車牌區域
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        image_cv = cv2.imread(car_image)
        plate_image_cv = image_cv[y1:y2, x1:x2]

        gray_cv = cv2.cvtColor(plate_image_cv, cv2.COLOR_BGR2GRAY)
        plate_image_pil = Image.fromarray(gray_cv)

        # 使用PaddleOCR進行OCR識別並取得車牌文字
        ocr_result = ocr.ocr(gray_cv)
        # 取得OCR結果的第一個元素
        if ocr_result and ocr_result[0]:
            raw_plate_text = ' '.join([line[1][0] for line in ocr_result[0]])

            # 修正OCR識別的車牌文字
            plate_text = correct_plate_text(raw_plate_text)

            print("車牌：", plate_text)
            plate_image_pil.show(title=f"License Plate: {plate_text}")
        else:
            print("未偵測到車牌")
