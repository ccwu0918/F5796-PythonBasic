# 參閱15-7頁

import os
from PIL import Image

# 合成浮水印的自訂函式
def watermark(src_dir='img', save_dir='thumb', logo_dir='logo', logo_img='swf_logo.png', size=600, margin=20):
    thumb_size = (size, size)
    logo_path = os.path.join(logo_dir, logo_img)
    logo = Image.open(logo_path)
    logo_w, logo_h = logo.size

    for f in os.listdir(src_dir):
        if f.endswith('.jpg'):
            img_path = os.path.join(src_dir, f)
            img = Image.open(img_path)
            img.thumbnail(thumb_size)
            
            img_w, img_h = img.size
            x = img_w - logo_w - margin
            y = img_h - logo_h - margin
            
            img.paste(logo, (x, y), logo)

            save_path = os.path.join(save_dir, f)
            img.save(save_path, quality=80)

if __name__ == '__main__':
    watermark()