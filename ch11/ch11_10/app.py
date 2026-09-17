from flask import Flask, render_template

app = Flask(__name__)

@app.route('/index.html')
@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/about/<user>')
def about(user):
    return render_template('index.html', name=user)

@app.route('/test/<int:score>')
def test(score):
    return render_template('score.html', score=score)

if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=True)
