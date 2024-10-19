from flask import Flask, redirect, render_template, request
from sqlalchemy_utils import database_exists, create_database

import pymysql
pymysql.install_as_MySQLdb() #workaround for mysqlclient, .whl files not being found on windows machines, using pymysql as a substitute for mysqldb

from src.models import db

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
def login():
    return render_template('login.html')