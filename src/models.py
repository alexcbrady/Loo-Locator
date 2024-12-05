from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)
    usern = db.Column(db.String(100), unique=True, nullable=False)
    passw = db.Column(db.String(255), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Building(db.Model):
    __tablename__ = 'building'

    building_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)

    bname = db.Column(db.String(100), unique=True, nullable=False)
    baddress = db.Column(db.String(100), unique=True, nullable=False)

class Review(db.Model):
    __tablename__ = 'review'

    review_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)

    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('building.building_id'), nullable=False)