from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def index():
    if not request.cookies.get('user'):
        res = make_response('設定Cookie…')
        res.set_cookie('user', 'Maker', max_age=60*3)
    else:
        usr = request.cookies['user']
        res = f'{usr}你好！'
    return res

if __name__ == "__main__":
    app.run('0.0.0.0', 80, debug=True)