from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/index.html')
@app.route('/')
def tea():
    return render_template('tea_form.html')

@app.route('/order', methods=['POST'])
def order():
    print('HTTP標頭：')
    print(request.headers)       # 顯示請求的標頭
    print('原始資料：')
    print(request.stream.read())  # 顯示收到的原始資料

    return "敬請再度光臨！"

if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=True)
