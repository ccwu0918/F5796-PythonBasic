# 參閱4-6頁

q_list = [
    '蘋果的英文？',
    '一打雞蛋用掉兩個，還剩下幾個？',
    '「問世間，情為何物？」的下一句？',
    '什麼話全世界通用？',
]

a_list = ['apple', '10', '直教生死相許', '電話']

score = 0
i = 0
total = len(q_list)

while i < total:
    q = q_list[i]
    a = a_list[i]
    i += 1

    print(q, end='  ')
    ans = input().lower().strip()

    if ans == a:
        score += 10
        print('好棒棒！')
    else:
        print('再接再厲～')

    print()

print('總分：', score)
