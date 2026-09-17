import argparse
import os
from os import path
import shutil
import sys

parser = argparse.ArgumentParser()
parser.add_argument("src", help="來源資料夾路徑")
parser.add_argument("dest", help="目標資料夾路徑")
args = parser.parse_args()

src = args.src   # 取得來源資料夾路徑
dest = args.dest # 取得目標資料夾路徑

if not path.isdir(src):  # 檢查來源資料夾是否存在
    print(f'"{src}" 不是資料夾路徑！')
    sys.exit(2)

if not path.isdir(dest):  # 檢查目標資料夾是否存在
    print(f'"{dest}" 不是資料夾路徑！')
    sys.exit(2)

for dir_path, dir_names, file_names in os.walk(src):
    # 計算 dir_path 相對於 src 的路徑
    rel_path = os.path.relpath(dir_path, src)

    # 當 dir_path 和 src 相同時，relpath() 會傳回 '.'
    if rel_path == '.':
        # 這是根目錄的情況
        dest_path = dest
        print(f'根目錄: {dest_path}')
    else:
        # 這是子目錄的情況
        dest_path = os.path.join(dest, rel_path)
        print(f'相對目錄: {rel_path}')
        print(f'子目錄: {dest_path}')
    
    # 確保目標資料夾存在
    os.makedirs(dest_path, exist_ok=True)

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
