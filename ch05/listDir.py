import os

path = r'D:\工作'  # 請自行修改路徑

for dir_path, dir_names, file_names in os.walk(path): 
    print('目前路徑：', dirPath)

    if len(dir_names) != 0:
        print('子目錄：', dir_names)
    else:
        print('這裡面沒有子目錄')

    if len(file_names) != 0:
        print('檔案：', file_names)
    else:
        print('這裡面沒有檔案')

    for f in file_names:
        print('檔案完整路徑：', os.path.join(dir_path, f))