score = 0  # 儲存成績的變數

q_list = [
    '蘋果的英文？',
    '一打雞蛋用掉兩個，還剩下幾個？',
    '什麼話全世界通用？',
]

a_list = ['apple', '10', '電話']

# len(q_list) 可以取得問題列表的長度 (這裡是 3)
# 所以 range(len(q_list)) 會產生 0, 1, 2
for i in range(len(q_list)):
    q = q_list[i]  # 取得第 i 個問題
    a = a_list[i]  # 取得第 i 個答案

    ans = input(q).lower().strip()

    if ans == a:
        score += 10
        print('好棒棒！')
    else:
        print(f'不對喔～答案是{ a }')

    print()

print(f'總分：{score}')
