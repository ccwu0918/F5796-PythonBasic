import re

pattern = r'\$\d+\.?\d{,2}'
text = '售價：$30.5元'
price = re.search(pattern, text).group()
print(price)

text = '折扣後價格12,799元 賣貴通報'
pattern = r'(\d+\,)?(\d+)'
price = re.search(pattern, text).group()
print('商品價格：', price)