# 參閱6-4頁
# 請先執行 pip install sympy

# 從 sympy 匯入 Symbol 和 solve 函式
from sympy import Symbol, solve
x = Symbol('x')    # 代表雞的數量
y = Symbol('y')    # 代表兔子的數量
total_heads = 35   # 頭的總數
total_feet = 94    # 腳的總數

eq1 = x + y - total_heads     # 建立方程式 1
eq2 = 2*x + 4*y - total_feet  # 建立方程式 2

solution = solve((eq1, eq2), (x, y))  # 解方程式
print("雞的數量:", solution[x])        # 取出 x 值
print("兔子的數量:", solution[y])      # 取出 y 值