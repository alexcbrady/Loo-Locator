from flask import Flask, redirect, render_template, request
from sqlalchemy_utils import database_exists, create_database

import pymysql
pymysql.install_as_MySQLdb() #workaround for mysqlclient, .whl files not being found on windows machines, using pymysql as a substitute for mysqldb

from src.models import db
from src.repositories.WebsiteRepository import website_repository_singleton

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3306/loodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI']) #for dev purposes, when actually deploying, we want to create a DB outside of the application

db.init_app(app)

@app.get('/')
def index_form():
    db.create_all()
    return render_template('index.html')

@app.get('/login')
def login_form():
    return render_template('login.html')

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
        #redirect to profile page
        website_repository_singleton.signup(username, email, password)
    #otherwise redirect back to signup page
    return redirect('/signup')