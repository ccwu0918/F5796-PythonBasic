class Order():
    total = 0
    price = 35

    def __init__(self, amount=1, spicy=False):
        self.amount = amount
        self.spicy = spicy
        Order.total += amount

    def check(self):
        sum = Order.price * self.amount
        sauce = '加辣' if self.spicy else '不加辣'
        print(f'{self.amount}個肉圓{sauce}，共{sum}元。')
