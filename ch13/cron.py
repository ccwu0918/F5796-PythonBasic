from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

count = 0

def hello():
    print(f'牛仔很忙，報時：{datetime.now()}')

def counter():
    global count
    count += 1
    print(f'數到3結束：{count}')

    if count == 3:
        sch.remove_job('job_counter')

sch = BlockingScheduler(timezone='Asia/Taipei') 
sch.add_job(hello,'interval', seconds=3)
# sch.add_job(hello,'interval', seconds=3, 
#                 start_date='2025-12-08 20:56:30',
#                 end_date='2025-12-08 20:57:00')
sch.add_job(counter,'interval', seconds=1, id='job_counter')

try:
    print('工作排程開始，按Ctrl+C結束。')
    sch.start()
except KeyboardInterrupt:
    sch.shutdown()
    print('工作排程結束～')
