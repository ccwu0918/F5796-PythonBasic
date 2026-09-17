from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/index.html')
@app.route('/')
def tea():
    return render_template('tea_form.html')

@app.route('/order', methods=['POST'])
def order():
    user = request.form['user']      # 大名
    sugar = request.form.get('sugar')  # 甜度
    area = request.form['area']       # 區域
    mix = request.form.getlist('mix')  # 加料

    return render_template("result.html",
                           user=user,
                           sugar=sugar,
                           mix=mix,
                           area=area)

if __name__ == '__main__':
    app.run()
