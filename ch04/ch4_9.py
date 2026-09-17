# 參閱4-12頁

print('比爾蓋茲創立了哪一家軟體公司？', end='  ')
ans = input().upper().strip()

if any([ans == '微軟', ans == 'MICROSOFT', ans == 'MS']):
    print('好棒棒！')
else:
    print('再接再厲～')
