# 參閱11-43頁

def wrapper(func):
    def inner(logs):
        return [func(d) for d in logs]
    return inner

@wrapper
def convert_date(log):
    return '/'.join([d for d in log.split('-')])

dates = [ '2026-10-07', '2027-08-24', '2028-03-21' ]  # 測試資料
log = convert_date(dates) # 傳回以"/"分隔的日期資料列表
print(log)