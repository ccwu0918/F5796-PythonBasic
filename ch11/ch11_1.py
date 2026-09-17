# 參閱11-7頁

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '歡迎光臨'

if __name__ == "__main__":
    app.run()