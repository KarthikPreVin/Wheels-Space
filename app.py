from flask import Flask,render_template
from controllers import *
from models import *
from mydb import db
import secrets
from datetime import datetime, timedelta



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True

app.secret_key = secrets.token_hex(16)
app.register_blueprint(auth_RBAC.auth_rbac)
app.register_blueprint(admin_routes.admin_routes)
app.register_blueprint(user_routes.user_routes)

db.init_app(app)
with app.app_context():
    db.create_all()
    # from sqlalchemy import inspect
    # print("TABLES: ",inspect(db.engine).get_table_names())
    check = Users.query.filter_by(email="admin@123")
    if check.count()==0:
        
        admin = Users(email = "admin@123", passw = "admin", name="ADMIN", address = "nil", pincode = 0)
        db.session.add(admin)
        db.session.commit()

        test_lot = Lots(
            location="Location1",
            price=20.00,
            address="123 Main St",
            pincode=600000,
            max_spots=15
        )
        test_lot_2 = Lots(
            location="Location2",
            price=30.00,
            address="456 Main St",
            pincode=600010,
            max_spots=20
        )
        db.session.add(test_lot)
        db.session.add(test_lot_2)
        db.session.commit()

        spots = []
        for i in range(15):
            spot_status = Status.O if i % 3==0 else Status.A
            spot = Spots(lot_id=test_lot.lot_id, status=spot_status)
            db.session.add(spot)
            spots.append(spot)
        spots_2=[]
        for i in range(20):
            spot_status = Status.O if i % 4==0 else Status.A
            spot = Spots(lot_id=test_lot_2.lot_id, status=spot_status)
            db.session.add(spot)
            spots_2.append(spot)
        db.session.commit()

        # 3. Add 5 Users
        users = []
        for i in range(5):
            user = Users(
                email=f"user{i+1}@example.com",
                passw="securepass",
                name=f"User {i+1}",
                address=f"{i+1} Street Lane",
                pincode=600001
            )
            db.session.add(user)
            users.append(user)
        db.session.commit()

        # 4. Add Reservations for the 5 Occupied spots
        now = datetime.now()
        for i in range(5):
            reservation = Reservations(
                spot_id=spots[i*3].spot_id,
                user_id=users[i].user_id,
                parking_timestamp=now - timedelta(hours=i),
                leaving_timestamp=None, 
                price_per_hour=test_lot.price,
                vehicle_number=f"AB{i}{i+1} DE{i}{i+1}{i+2}{i+4}"
            )#type: ignore
            db.session.add(reservation)
            reservation = Reservations(
                spot_id=spots_2[i*4].spot_id,
                user_id=users[i].user_id,
                parking_timestamp=now - timedelta(hours=i),
                leaving_timestamp=None,
                price_per_hour=test_lot_2.price,
                vehicle_number=f"AB{i*10} BC{(i+1)*10}{i+2}{i+4}"
            )
            db.session.add(reservation)
            
        db.session.commit()

@app.route("/")
def main():
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)
