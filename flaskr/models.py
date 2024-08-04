""" DBのtable設計とCRUDメソッド群 """

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user
from flaskr.views import app
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime
import os

DB_URI = 'postgresql://postgres:PASSWORD@localhost/flask_sns'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'SECRET'

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    """ LoginManagerをDBに対して動作させるためのメソッド """
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    """ ログインセッションを管理するUserテーブル """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    email = db.Column(db.String(32), index=True, unique=True)
    password = db.Column(db.Text)
    comment = db.Column(db.Text, default='')
    picture_path = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)  # login_managerで必要
    create_at = db.Column(db.DateTime, default=datetime.now)  # datetime.now()では変になる
    update_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, email, password):
        """ ユーザ名、メール、パスワードが入力必須 """
        self.username = username
        self.email = email
        self.password = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """ パスワードをチェックしてTrue/Falseを返す """
        return check_password_hash(self.password, password)

    def reset_password(self, password):
        """ 再設定されたパスワードをDBにアップデート """
        self.password = generate_password_hash(password).decode('utf-8')

    @classmethod
    def select_by_email(cls, email):
        """ UserテーブルからemailでSELECTされたインスタンスを返す """
        return cls.query.filter_by(email=email).first()

