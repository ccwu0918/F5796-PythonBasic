# 參閱11-19頁

from flask import Flask, url_for, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return '歡迎光臨～'

@app.route('/prod/<int:id>/')
def product(id):
    return '#{} 商品的展示頁'.format(id)

@app.route('/best_sell/')
def best_sell():
    return redirect(url_for('product', id=109))

if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=True)
