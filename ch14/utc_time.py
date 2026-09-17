from datetime import datetime, timezone, timedelta

utc_zone = timezone.utc  # 定義時區
tw_zone = timezone(timedelta(hours=8))  # 台灣時區 UTC+8

utc = datetime.now(tz=utc_zone)  # 取得 UTC 時間
print('轉換前：', utc.strftime('%Y/%m/%d %H:%M'))

tw_time = utc.astimezone(tw_zone) # 轉換為台灣時間
print('轉換後：', tw_time.strftime('%Y/%m/%d %H:%M'))