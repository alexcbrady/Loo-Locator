from src.models import db, User, Building, Review

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

    def newReview(self, title, body, rating, user_id, building_id):
        newReview = Review(title=title, body=body, rating=rating, user_id=user_id, building_id=building_id)
        db.session.add(newReview)
        db.session.commit()
        return None

    def editReview(self, title, body, rating, user_id, building_id, review_id):
        foundReview = Review.query.filter_by(review_id = review_id).first()
        foundReview.title = title
        foundReview.body = body
        foundReview.rating = rating
        foundReview.user_id = user_id
        foundReview.building_id = building_id
        db.session.flush()
        db.session.commit()
        return None 

    def viewReview(self, review_id):
        foundReview = Review.query.filter_by(review_id = review_id).first()
        return foundReview

    def profileReviews(self, user_id):
        foundReviews = Review.query.filter_by(user_id = user_id)
        return foundReviews

    def buildingReviews(self, building_id):
        foundReviews = Review.query.filter_by(building_id = building_id)
        return foundReviews

    def averageRating(self, building_id):
        foundReviews = Review.query.filter_by(building_id = building_id)
        total = 0
        count = 0
        for review in foundReviews:
            total += review.rating
            count += 1
        if (count == 0):
            return "test"
        else:
            average = total/count
        return average
            

website_repository_singleton = WebsiteRepository()