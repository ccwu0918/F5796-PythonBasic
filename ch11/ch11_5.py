# 參閱11-18頁

import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    app.logger.debug('這是來自偵錯的訊息')
    app.logger.info('使用者進入首頁')
    app.logger.warning('注意：這個API即將被棄用')
    app.logger.error('糟了～無法連接資料庫')

    return '歡迎光臨'

if __name__ == "__main__":
    app.logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler('app.log', maxBytes=100*1024, backupCount=3)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s [%(filename)s:%(lineno)d]'
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run(debug=True, host='0.0.0.0', port=80)
