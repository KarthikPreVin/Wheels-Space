from flask_sqlalchemy import SQLAlchemy
from mydb import db

class Reservations(db.Model):
    __tablename__ = "Reservations"
    reservation_id = db.Column(db.Integer, primary_key = True)
    spot_id = db.Column(db.Integer, db.ForeignKey("Spots.spot_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    Parking_timestamp = db.Column(db.DateTime, nullable = False)
    Leaving_timestamp = db.Column(db.DateTime, nullable = False)
    price_per_hour = db.Column(db.Numeric(10, 2), nullable=False)

    spot = db.relationship("Spots", back_populates = "reservation")
    user = db.relationship("Users", back_populates = "reserved")
