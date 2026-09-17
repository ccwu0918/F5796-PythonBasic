# 參閱11-42頁

def price_tax(t):
    def tax(d):
        return d * t
    return tax

price = price_tax(1.05)
print('含稅價：', price(100))
print('含稅價：', price(150))