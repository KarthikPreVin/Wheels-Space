from mydb import db

class Reservations(db.Model):
    __tablename__ = "Reservations"
    reservation_id = db.Column(db.Integer, primary_key = True)
    spot_id = db.Column(db.Integer, db.ForeignKey("Spots.spot_id"), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    parking_timestamp = db.Column(db.DateTime, nullable = False)
    leaving_timestamp = db.Column(db.DateTime)
    price_per_hour = db.Column(db.Numeric(10, 2), nullable=False)
    vehicle_number = db.Column(db.String(11), nullable=False)

    spot = db.relationship("Spots", back_populates = "reservation")
    user = db.relationship("Users", back_populates = "reserved")
