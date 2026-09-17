import re

text = '電子郵件：cubie@example.com'
pattern = r'[\w.-]+@[^@\s.]+\.[a-zA-Z]{2,10}$'  # [\w.-]+@[\w.-]+
match = re.search(pattern, text)

if match:
    print ('找到：', match.group())
else:
    print ('找不到吻合的內容')