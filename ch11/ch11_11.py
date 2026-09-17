# 參閱11-41頁

def bar():
    a = 10
    def inner(n):
      b = a + n
      print(b)
    return inner

f = bar()
f(5)  # 印出15