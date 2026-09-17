class Order():
    total = 0
    __price = 35  # 價格
    __number = 0  # 取餐編號

    def __init__(self, amount=1, spicy=False):
        self._amount = amount
        self._spicy = spicy

        Order.__number += 1
        self.__number = Order.__number
        Order.total += amount

    @property
    def number(self):  # 查看取餐編號
        return self.__number

    @property
    def amount(self):  # 查看數量
        return self._amount

    @amount.setter
    def amount(self, n):  # 修改數量
        Order.total -= self._amount
        Order.total += n
        self._amount = n

    @staticmethod
    def quote():   # 請老闆報價
        print(f'肉圓一個{Order.__price}元，加不加醬講清楚！')

    def check(self):
        sum = Order.__price * self._amount
        sauce = '加醬' if self._spicy else '不加醬'
        print(f'{self._amount}個肉圓{sauce}，共{sum}元。')

    def __str__(self):
        sauce = '加醬' if self._spicy else '不加醬'
        return f'{self._amount}個肉圓{sauce}'

    def __repr__(self):
        return f'{self.__class__}, amount:{self._amount},spicy:{self._spicy}'
