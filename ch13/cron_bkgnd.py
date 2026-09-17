from apscheduler.schedulers.background import BackgroundScheduler
import os
import time

def hello():
    print('你好！')

if __name__ == '__main__':
    sch = BackgroundScheduler()
    sch.add_job(hello,'interval', seconds=3)
    sch.start()
    print('工作排程開始，按Ctrl+C結束。')
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sch.shutdown()
        print('工作排程結束～')