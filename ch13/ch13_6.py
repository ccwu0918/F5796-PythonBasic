# 參閱13-35頁

events = [
    {"type": "濕度", "value": 7},   # 濕度 7%
    {"type": "溫度", "value": 33},  # 室溫 33°C
    {"type": "溫度", "value": 24},
    {"type": "窗簾", "room":"主臥", "value": 50}, # 窗簾開啟 50%
    {"type": "照度", "room":"客廳", "lux": 120}, # 客廳照度 120 lux
]

def handle_event(evt):
    match evt:
        case {"type": "溫度", "value": temp} if temp > 30:
            print(f"{temp}°C，好熱啊，請開空調～")
        case {"type": "溫度", "value": temp}:
            print(f"室內  {temp}°C")
        case {"type": "濕度", "value": h} if h < 10:
            print(f"濕度 {h}%，好渴啊～請澆水！")
        case {"type": "濕度", "value": h}:
            print(f"濕度 {h}%")
        case {"type": "照度", "room": room, "lux":lux}:
            print(f"{room} 照度 {lux}")
        case _:   # 處理其他格式資料
            print("偵測到未知的事件")

for e in events:  # 逐一取出 events 列表裡的每個感測資料
    handle_event(e)