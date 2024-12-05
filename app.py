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

MARKERS_DICT = {
    'WOODWARD': '&markers=color:green%7Clabel:W%7CWoodward+Hall,+Charlotte,+NC',
    'FRETWELL': '&markers=color:green%7Clabel:F%7CFretwell,+Charlotte,+NC',
    'LIBRARY': '&markers=color:green%7Clabel:L%7CJ.+Murrey+Atkins+Library'
}

MARKERS = ''
for key in MARKERS_DICT:
    MARKERS += MARKERS_DICT[key]

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
    return render_template('main.html',API_KEY=API_KEY,MARKERS=MARKERS)

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
   return render_template('account.html', account=session.get('user')) 

@app.get('/building')
def building_form():
    building = website_repository_singleton.findBuilding(request.args.get('button', 'default'))
    return render_template('building.html', building=building)

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