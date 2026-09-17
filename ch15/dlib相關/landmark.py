import face_recognition as fr
from PIL import Image, ImageDraw

feature_name = {
             'chin':'下巴', 'left_eyebrow':'左眉', 'right_eyebrow':'右眉', 
             'nose_bridge':'鼻樑', 'nose_tip':'鼻尖', 'left_eye':'左眼', 
             'right_eye':'右眼', 'top_lip':'上唇', 'bottom_lip':'下唇'}

img_path = 'pict\sophia.jpg'
img = fr.load_image_file(img_path)  # Numpy陣列
face_list = fr.face_landmarks(img)

print("在相片中找到{}張臉".format(len(face_list)))

pil_img = Image.fromarray(img)
d = ImageDraw.Draw(pil_img)

for marks in face_list:
    for f in marks.keys():
        print("{}的特徵座標：{}".format(feature_name[f], marks[f]))
        d.line(marks[f], width=5)

pil_img.show()
