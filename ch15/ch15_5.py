# 參閱15-14頁

import numpy as np
from PIL import Image

img = Image.open(r'img\jump.jpg')
img_arr = np.array(img)

bright = int(255 * 0.3)
bright_arr = np.where((255-img_arr) < bright, 255, img_arr+bright)
pil_image = Image.fromarray(bright_arr)
pil_image.show()