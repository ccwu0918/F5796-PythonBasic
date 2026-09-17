# 參閱4-8頁

print('請輸入數字：', end='  ')
ans = input()

while not ans.isdigit():
    print('請輸入數字：', end='  ')
    ans = input()

print('剩下', ans, '個')
