from guestbook import app, db

with app.app_context():
    db.create_all()
    print("資料庫資料表已成功建立。")