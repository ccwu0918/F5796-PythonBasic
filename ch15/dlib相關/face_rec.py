import face_recognition as fr
from PIL import Image, ImageDraw, ImageFont
import pickle

dataset_file = 'dataset\\staff.dat'             # 請自行修改路徑
font_file = "font\\NotoSansCJKtc-Regular.otf"   # 請自行修改路徑
_font = ImageFont.truetype(font_file, 15) 

with open(dataset_file, 'rb') as f:
    d = pickle.load(f)
    face_encodings = d['encode']
    face_names = d['name']

photo = fr.load_image_file("pict\\people.jpg")  # 請自行修改路徑
people_locs = fr.face_locations(photo)
people_encs = fr.face_encodings(photo, people_locs)

pil_image = Image.fromarray(photo)
draw = ImageDraw.Draw(pil_image)

for (top, right, bottom, left), encoding in zip(people_locs, people_encs):
    matches = fr.compare_faces(face_encodings, encoding, tolerance=0.4)
    name = "路人甲"

    if True in matches:
        first_match_index = matches.index(True)
        name = face_names[first_match_index]

    draw.rectangle(((left, top), (right, bottom)), outline='blue')  # (0, 0, 255)
    txt_w, txt_h = draw.textsize(name, font=_font)
    draw.rectangle(((left, bottom + txt_h + 10), (right, bottom)), fill='blue', outline='blue')
    draw.text((left + 8, bottom + 5), name, fill='white', font=_font) # (255, 255, 255, 255)

del draw

pil_image.show()