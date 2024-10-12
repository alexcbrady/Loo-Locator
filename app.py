from flask import Flask, redirect, render_template, request

import pymysql

import os

app = Flask(__name__)

conn = pymysql.connect(
    host = 'localhost',
    user = 'root',
    passw = os.environ.get('MY_SQL_PASSWORD'),
    db = 'loodb'
)

cursor = conn.cursor()

