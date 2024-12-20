from flask import Flask, redirect, render_template, request, session
from sqlalchemy_utils import database_exists, create_database
import os
from dotenv import load_dotenv

import pymysql
pymysql.install_as_MySQLdb() #workaround for mysqlclient, .whl files not being found on windows machines, using pymysql as a substitute for mysqldb

from src.models import db
from src.repositories.WebsiteRepository import website_repository_singleton

app = Flask(__name__)
# a secret key for securely signing the session cookie, essential for logout feature
app.secret_key = os.urandom(24)  # Generate a random secret key

load_dotenv()
DB_PASSWORD = os.getenv('DB_PASSWORD')
API_KEY = os.getenv('API_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root:{DB_PASSWORD}@localhost:3306/loodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI']) #for dev purposes, when actually deploying, we want to create a DB outside of the application

db.init_app(app)

@app.get('/')
def index_form():
    db.create_all()
    website_repository_singleton.buildings()
    return render_template('index.html')

@app.get('/main')
def main_form():
    return render_template('main.html',API_KEY=API_KEY)

@app.get('/signin')
def login_form():
    return render_template('login.html')

@app.post('/signin')
def login():
    #retrieve credentials from form
    username = request.form.get('username')
    password = request.form.get('password')

    #if login returns something, redirect to main page
    #needs additional work to set the logined user to be "active"
    user = website_repository_singleton.signin(username, password)
    if (user):
        #serializes the found user into the session
        session['user'] = user.as_dict()
        return redirect('/main')
    #otherwise, redirect back to singin page to try again
    else:
        error_message = "Invalid username or password. Please try again."
        return render_template('login.html', error_message=error_message)

@app.get('/signup')
def signup_form():
    return render_template('signup.html')

@app.post('/signup')
def signup():
    #retrieve credentials from form
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    #if a user tries to sign up with credentials that do not already have a user
    if (website_repository_singleton.findUser(username, email) == None):
        #add user to db, then redirect to main page
        #needs additional work to set the registerd user to be "active"
        newUser = website_repository_singleton.signup(username, email, password)
        session['user'] = newUser.as_dict()
        return redirect('/main')
    #otherwise redirect back to signup page
    return redirect('/signup')

@app.get('/logout')
def logout():
    session.clear()  # Clear all session data
    return redirect('/')

@app.get('/account')
def account():
    reviews = website_repository_singleton.profileReviews(session.get('user')['user_id'])
    return render_template('account.html', account=session.get('user'), reviews=reviews) 

@app.route('/update_account', methods=['GET', 'POST'])
def update_account():
    if request.method == 'POST':
        # Retrieve form data
        new_username = request.form.get('username')  
        # Update the user in the database 
        user_id = session.get('user')['user_id']
        website_repository_singleton.updateUser(user_id, new_username)

        # Update session to reflect the new username
        session['user']['username'] = new_username  # Corrected key name here

        # Redirect or display a success message
        return redirect('/account')  # Redirect to account page after successful update
    
    # Render the update account page for GET requests
    return render_template('update_account.html')

@app.get('/building')
def building_form():
    building = website_repository_singleton.findBuilding(request.args.get('button', 'default'))
    reviews = website_repository_singleton.buildingReviews(building.building_id)
    averageRating = website_repository_singleton.averageRating(building.building_id)
    return render_template('building.html', building=building, reviews=reviews, averageRating=averageRating)

@app.get('/review')
def new_form():
    return render_template('review.html')

@app.post('/review')
def new():
    title = request.form.get('review_title')
    body = request.form.get('review_body')
    rating = request.form.get('review_rating')
    building = request.form.get('review_building')

    building_id = website_repository_singleton.findBuilding(building).building_id
    user_id = website_repository_singleton.findUser(session.get('user')['usern'], session.get('user')['email']).user_id

    website_repository_singleton.newReview(title, body, rating, user_id, building_id) 

    return redirect('/main')

@app.get('/about')
def about_form():
    return render_template('about.html')
 
@app.get('/about2')
def about2_form():
    return render_template('about2.html')

@app.get('/testimonial')
def testimonial_form():
    return render_template('testimonial.html')

@app.get('/review/<int:review_id>')
def view_form(review_id):
    review = website_repository_singleton.viewReview(review_id=review_id)
    if review.user_id == session.get('user')['user_id']:
        editable = True
    else:
        editable = False
    return render_template('viewReview.html', review=review, editable=editable)

@app.get('/review/<int:review_id>/edit')
def edit_form(review_id):
    review = website_repository_singleton.viewReview(review_id=review_id)
    return render_template('review.html', review=review)

@app.post('/review/<int:review_id>/edit')
def edit(review_id):
    title = request.form.get('review_title')
    body = request.form.get('review_body')
    rating = request.form.get('review_rating')
    building = request.form.get('review_building')

    building_id = website_repository_singleton.findBuilding(building).building_id
    user_id = website_repository_singleton.findUser(session.get('user')['usern'], session.get('user')['email']).user_id

    website_repository_singleton.editReview(title, body, rating, user_id, building_id, review_id) 

    return redirect('/main')