# 參閱11-10頁

from flask import Flask

app = Flask(__name__)

@app.route('/index.html')
@app.route('/')
def index():
    return '''
    <html>
      <head>
        <meta charset="utf-8">
        <title>世說鮮語</title>
      </head>
      <body>
        人家有的是背景，而我有的只是背影…
      </body>
    </html>
    '''


@app.route('/about')
def about():
    return '關於我們'


@app.route('/faq/')
def faq():
    return '問答集'


if __name__ == '__main__':
    app.run()
