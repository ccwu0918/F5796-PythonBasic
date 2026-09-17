# 參閱3-19頁

id = 17
name = '小趙'

print("姓名：%s" % name)
print("姓名：%s，座號：%d" % (name, id))

num = 70.8
print("海洋佔了地球表面的%.2f%%" % num)

msg = '{0} 今年 {1} 歲。'
msg = msg.format('小趙', 10)
print(msg)

print('體積縮小{:.3f}%'.format(33.45678))

print('氮氣佔空氣體積{0:.0f}%，氧氣佔{1:.2f}%。'.format(78.08, 20.95))

print('{:5},{:^8},{:5d}'.format(12, 34, 56))

print('{:=^40s}'.format('傳說中的分隔線'))

r = 9
print(f'若半徑={r}，圓面積={3.14*r**2}')

txt = '我是分隔線'
print(f'{txt:=^30}')
