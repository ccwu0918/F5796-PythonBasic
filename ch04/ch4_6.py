# 參閱4-9頁

q_list = [
    '蘋果的英文？',
    '一打雞蛋用掉兩個，還剩下幾個？',
    '什麼話全世界通用？',
]

a_list = ['apple', '10', '電話']

score = 0

for q, a in zip(q_list, a_list):
    print(q, end='  ')
    ans = input().lower().strip()

    if ans == a:
        score += 10
        print('答對了！')
    else:
        print('答錯了！答案是', a)

    print()

print('總分：', score)
