from src.models import db, User

class WebsiteRepository:

    def findUser(self, username, email):
        foundUser = User.query.filter_by(email = email, usern = username).first()
        return foundUser

    def signup(self, username, email, password):
        newUser = User(email = email, usern = username, passw = password)
        db.session.add(newUser)
        db.session.commit()
        return newUser
    
website_repository_singleton = WebsiteRepository()