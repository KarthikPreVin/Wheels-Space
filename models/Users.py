from flask_sqlalchemy import SQLAlchemy
from mydb import db

class Users(db.Model):
    __tablename__ = "Users"
    user_id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique = True, nullable=False)
    passw = db.Column(db.String(32), nullable = False)

    reserved = db.relationship("Reservations",back_populates = "user")
