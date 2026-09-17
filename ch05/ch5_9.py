# 參閱5-20頁

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("url", help="指定YouTube視訊網址")

args = parser.parse_args()
print('視訊網址：', args.url)
