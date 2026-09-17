# 參閱4-16頁

import argparse
import os
from os import path
import shutil
import sys

parser = argparse.ArgumentParser()
parser.add_argument("src", help="來源資料夾路徑")
parser.add_argument("dest", help="目標資料夾路徑")
args = parser.parse_args()

if path.isdir(args.src):
    src = path.join(args.src, '')
else:
    print('"{}" 不是資料夾路徑！'.format(src))
    sys.exit(2)

if path.isdir(args.dest):
    dest = path.join(args.dest, '')
else:
    print('"{}" 不是資料夾路徑！'.format(dest))
    sys.exit(2)

for dir_path, dir_names, file_names in os.walk(src):
    folder = dir_path.replace(src, '')
    dest_path = dest  # 目標路徑
    print('目前路徑：', dir_path)

    if folder == '':
        print('目前在根目錄')
    else:
        print('資料夾路徑：', folder)
        dest_path = path.join(dest, folder)

        if not path.isdir(dest_path):
            print('新增資料夾：', dest_path)
            os.makedirs(dest_path)   # 新增資料夾

    for f in file_names:
        src_path = path.join(dir_path, f)
        save_path = path.join(dest_path, f)

        if not path.isfile(save_path):
            shutil.copy2(src_path, save_path)
        else:
            src_time = int(path.getmtime(src_path))
            dest_time = int(path.getmtime(save_path))

            if src_time > dest_time:
                shutil.copy2(src_path, save_path)
