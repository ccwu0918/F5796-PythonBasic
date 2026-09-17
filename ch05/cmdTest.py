import argparse

parser = argparse.ArgumentParser()  # 建立解析命令的物件

parser.add_argument('src', help="來源資料夾路徑")
parser.add_argument('dest', help="目標資料夾路徑")

args = parser.parse_args()  # 解析命令參數
print('來源路徑：', args.src)
print('目標路徑：', args.dest)