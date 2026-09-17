from datetime import timedelta
from flask import (Flask, redirect, render_template,
                   request, session, url_for, make_response)

app = Flask(__name__)
app.config['SECRET_KEY'] = b'my_very_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=3)

# @app.route('/')
# def index():
#     if not request.cookies.get('user'):
#         res = make_response('設定Cookie…')
#         res.set_cookie('user', 'Maker', max_age=60*3)
#     else:
#         usr = request.cookies['user']
#         res = f'{usr}你好！'
#     return res

@app.route('/')
def index():
    if 'user' in session:
        usr = session['user']
        return f'歡迎回來，{usr}！\
                <br><a href="/logout">登出</a>'
    return '路人甲你好！'

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['user'] = request.form['user']
        # session.permanent = True
        return redirect(url_for('index'))
    return render_template('login_session.html')

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run('0.0.0.0', 80, debug=True)