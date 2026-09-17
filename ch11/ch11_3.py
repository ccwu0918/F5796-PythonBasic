# 參閱11-11頁

from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    print(xyz)  # 輸出xyz變數值
    return '歡迎光臨～'

if __name__ == '__main__':
    app.run(debug=True)