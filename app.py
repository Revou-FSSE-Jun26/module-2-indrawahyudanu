form flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234567@localhost/revoshop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class user(db.model):
    __tablename__='users'
    id = db.column(db interger, primary_key=True)
    username = db.column(db.string(100))
    email = db.column(db.string(255))
    created_at =

class product(db.model):
    __tablename__ = 'produtcs'
    id = db.column(db interger, primary_key=True)
    name = db.column(db.string(100))
    price = db.column(db.numeric(10, 2))






