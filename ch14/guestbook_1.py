from datetime import datetime, timezone, timedelta
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import re
from markupsafe import escape, Markup

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bbs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# # 註冊自訂的過濾器
# @app.template_filter('nl2br')
# def nl2br_filter(text):
#     """將換行符號轉換為 HTML <br> 標籤"""
#     if text is None:
#         return ''
#     return text.replace('\n', '<br>\n')

# _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
# @app.template_filter()
# @evalcontextfilter
# def nl2br(eval_ctx, value):
#     escaped_value = escape(value)
#     paragraphs = _paragraph_re.split(escaped_value)
#     result_parts = []
#     for p in paragraphs:  # 處理每個段落
#         p_with_br = p.replace('\n', Markup('<br>\n'))
#         result_parts.append(f'<p>{p_with_br}</p>')
    
#     result = '\n\n'.join(result_parts)
    
#     if eval_ctx.autoescape:
#         result = Markup(result)
#     return result

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')
@app.template_filter('nl2br')
def nl2br_filter(value: str) -> Markup:
    if value is None:
        return Markup('')
    
    escaped_value = escape(str(value))
    paragraphs = filter(None, _paragraph_re.split(escaped_value))
    
    result_parts = [
        f'<p>{p.replace(chr(10), Markup("<br>"))}</p>' 
        for p in paragraphs
    ]

    result = '\n\n'.join(result_parts)
    return Markup(result)

@app.template_filter('datetimefilter')
def datetime_filter(dt):
    """格式化日期時間為台灣時間"""
    if dt is None:  # 若無傳入dt參數
        return ''   # 則傳回空字串
    tw_zone = timezone( timedelta(hours=8) )
    t = dt.astimezone( tw_zone ) # 轉換為台灣時間
    return t.strftime('%Y/%m/%d %H:%M:%S')

class Guestbook(db.Model):  # 留言板資料表
    id = db.Column(db.Integer, primary_key=True)
    guestname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    message = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(10), nullable=False, 
        default='ico1.png')
    postdate = db.Column(db.DateTime, nullable=False,
        default=lambda: datetime.now(timezone.utc)) # 使用UTC時間

    def __repr__(self):
        return 'guestname:{},email:{},postdate:{}'.format(
            self.guestname, 
            self.email,
            self.postdate
        )

class User(UserMixin, db.Model):  # 使用者資料表
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    pwd_hash = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def verify_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    @property
    def password(self):
        raise AttributeError('無法讀取password屬性')

    @password.setter
    def password(self, password):
        self.pwd_hash = generate_password_hash(password)
    
    def __repr__(self):
        return f'name:{self.name},email:{self.email}'

@app.route('/')
def index():
    gb = Guestbook.query.all()
    return render_template("index.html", books=gb)

@app.route('/add_msg', methods=['POST'])
def add_msg():
    # 取得表單資料
    guestname = request.form.get('guestname')
    email = request.form.get('email')
    message = request.form.get('message')
    icon = request.form.get('icon', 'ico1.png')
    
    # 建立新的留言記錄
    new_msg = Guestbook(
        guestname=guestname,
        email=email,
        message=message,
        icon=icon
    )
    
    # 儲存到資料庫
    db.session.add(new_msg)
    db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 建立所有資料表
    app.run('0.0.0.0', 80, debug=True)