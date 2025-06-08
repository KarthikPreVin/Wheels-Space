from flask_sqlalchemy import SQLAlchemy
from mydb import db

class Users(db.Model):
    __tablename__ = "Users"
    user_id = db.Column(db.Integer, primary_key = True)
    email   = db.Column(db.String(64), unique = True, nullable=False)
    passw   = db.Column(db.String(32), nullable = False)
    name    = db.Column(db.String(64), nullable = False)
    address = db.Column(db.Text, nullable = False)
    pincode = db.Column(db.Integer,nullable = False)

    reserved = db.relationship("Reservations",back_populates = "user")
