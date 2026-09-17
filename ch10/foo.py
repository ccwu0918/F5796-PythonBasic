def A():
    print('執行A函式')


def B():
    print('執行B函式')


print('__name__的值是', __name__)
if __name__ == '__main__':
    A()
else:
    B()
