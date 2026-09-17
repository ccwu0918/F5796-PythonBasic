# 參閱4-9頁

print('比爾蓋茲創立了哪一家軟體公司？', end='  ')
corrects = ['微軟', 'MICROSOFT', 'MS']   # 正確解答列表
ans = input().upper().strip()

if ans in corrects:
    print('好棒棒！')
else:
    print('再接再厲～')
