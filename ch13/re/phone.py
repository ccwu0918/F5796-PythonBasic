import re

text = '聯絡電話：0912345678，夜間關機。'

# pattern = r'09\d{8}'
pattern = r'(?:0|886-?)9\d{2}-?\d{6}'
match = re.search(pattern, text)

if match:
    print ('找到：', match.group())
else:
    print ('找不到吻合的內容')