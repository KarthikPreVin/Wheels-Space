import enum
from mydb import db

class Status(enum.Enum):
    O = "Occupied"
    A = "Available"
    

class Spots(db.Model):
    __tablename__ = "Spots"
    spot_id = db.Column(db.Integer, primary_key = True)
    lot_id = db.Column(db.Integer, db.ForeignKey("Lots.lot_id"))
    status = db.Column(db.Enum(Status),nullable=False, default = Status.A)
    
    lot = db.relationship("Lots",back_populates = "spots")
    reservation = db.relationship("Reservations", back_populates = "spot")

#access as spots.status.value as spots.status = Status.O, but spots.status.value = "occupied"