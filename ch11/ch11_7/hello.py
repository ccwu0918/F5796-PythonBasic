from flask import Flask

app = Flask(__name__)

@app.route('/index.html')
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=True)
