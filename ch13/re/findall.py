import re

pattern = r'(?:0|886-?)9\d{2}-?\d{6}'
text = '電話1：886-912-345678；電話2：0911-234567'
phones = re.findall(pattern, text)
print(phones)