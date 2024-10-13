from flask_sqlalchemy import  SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    email = db.Column(db.String, unique=True)
    usern = db.Column(db.String, unique=True)
    passw = db.Column(db.String)
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
