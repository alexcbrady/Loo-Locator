from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)
    usern = db.Column(db.String(100), unique=True, nullable=False)
    passw = db.Column(db.String(255), nullable=False)

class Building(db.Model):
    __tablename__ = 'building'

    building_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)

    bname = db.Column(db.String(100), unique=True, nullable=False)
    baddress = db.Column(db.String(100), unique=True, nullable=False)