# 參閱11-15頁

import logging  # 引用 Python 內建的「日誌」套件
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    app.logger.debug('這是來自偵錯的訊息')
    app.logger.info('用戶進入首頁')
    app.logger.warning('注意：這個API即將被棄用')
    app.logger.error('糟了～無法連接資料庫')
    return '歡迎光臨'
    
if __name__ == "__main__":
    app.logger.setLevel(logging.WARNING)
    app.run(debug=True, host='0.0.0.0', port=80)