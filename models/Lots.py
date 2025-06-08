from flask_sqlalchemy import SQLAlchemy
from mydb import db

class Lots(db.Model):
    __tablename__ = "Lots"
    lot_id   = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(30), unique = True, nullable=False)
    price    = db.Column(db.Numeric(10, 2), nullable=False)
    address  = db.Column(db.String(100), nullable = False)
    pincode  = db.Column(db.Integer, nullable=False)
    max_spots= db.Column(db.Integer, nullable=False)

    spots    = db.relationship("Spots",back_populates = "lot")