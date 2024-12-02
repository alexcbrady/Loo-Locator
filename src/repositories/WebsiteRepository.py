from src.models import db, User, Building

class WebsiteRepository:

    #initalize buildings table
    def buildings(self):
        if Building.query.first() == None:
            buildings = [
                Building(bname = "Woodward Hall", baddress = "8723 Cameron Blvd, Charlotte, NC 28262"),
                Building(bname = "Fretwell", baddress = "Charlotte, NC 28262"),
                Building(bname = "J. Murrey Atkins Library", baddress = "9201 University City Blvd, Charlotte, NC 28223")
            ]
            db.session.bulk_save_objects(buildings)
            db.session.commit()
        else:
            return None

    def findUser(self, username, email):
        foundUser = User.query.filter_by(email = email, usern = username).first()
        return foundUser

    def signup(self, username, email, password):
        newUser = User(email = email, usern = username, passw = password)
        db.session.add(newUser)
        db.session.commit()
        return newUser
    
    def signin(self, username, password):
        foundUser = User.query.filter_by(usern = username).first()
        if (foundUser):
            if (foundUser.passw == password):
                return foundUser
            else:
                return None
        else:
            return None
    
    def findBuilding(self, building_name):
        foundBuilding = Building.query.filter_by(bname = building_name).first()
        #shouldn't require error handling since this is just used on clicks of predetermined buttons
        return foundBuilding
    
website_repository_singleton = WebsiteRepository()