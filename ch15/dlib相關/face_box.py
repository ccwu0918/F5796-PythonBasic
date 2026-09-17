import face_recognition as fr
from PIL import Image, ImageDraw

img = fr.load_image_file(r"img\kids.jpg")
face_loc = fr.face_locations(img)
pil_img = Image.fromarray(img)

for loc in face_loc:
    top, right, bottom, left = loc
    draw = ImageDraw.Draw(pil_img)
    draw.rectangle([left, top, right, bottom], outline="blue")

pil_img.show()