from datetime import datetime
from flask import Blueprint, session, url_for, render_template, redirect, request

from models import *
from mydb import db
from sqlalchemy import text


user_routes = Blueprint("user_routes",__name__)

@user_routes.route("/home/<int:user_id>")
def home(user_id):
    user = Users.query.filter_by(user_id = user_id).first()
    raw_sql =  text(f"""SELECT 
                            spots.spot_id, 
                            lots.location, 
                            reservations.vehicle_number, 
                            reservations.parking_timestamp, 
                            reservations.leaving_timestamp
                        FROM reservations 
                        LEFT OUTER JOIN spots ON (reservations.spot_id = spots.spot_id)
                        JOIN lots ON (spots.lot_id=lots.lot_id)
                        JOIN users ON (users.user_id = reservations.user_id)
                        WHERE users.user_id = {user_id};""")
    res = db.session.execute(raw_sql).all()
    #ordering
    i=len(res)-1
    ind = i
    while i>=0:
        if res[ind].leaving_timestamp==None:
            res.insert(0,res.pop(ind))
            ind+=1
        i-=1
        ind-=1

    # print([i.leaving_timestamp for i in res])
    # for i in res[0]:
    #     print(i, type(i))
    # returns: [(1, 'Adambakkam 2', 'AB01 DE0124', '2025-06-12 19:43:18.681450', None), (2, 'Location2', 'AB0 BC1024', '2025-06-12 19:43:18.681450', None)]
    # 1 <class 'int'>
    # Adambakkam 2 <class 'str'>
    # AB01 DE0124 <class 'str'>
    # 2025-06-12 19:43:18.681450 <class 'str'>
    # None <class 'NoneType'>
    # print(res[0].lot_id, res[0].location, res[0].vehicle_number, res[0].parking_timestamp, )
    return render_template("user_login.html", user = user, reservations = res)

@user_routes.route("/releasespot/<int:user_id>/<int:spot_id>")
def releasespot(user_id, spot_id):
    #check who is releasing spot
    user = Users.query.filter_by(user_id = user_id).first()
    spot = Spots.query.filter_by(spot_id=spot_id).first()
    lot = spot.lot
    reservation = Reservations.query.filter_by(spot_id = spot.spot_id, leaving_timestamp=None).first()

    return render_template("user_release_spot.html", user = user, lot = lot, spot_id = spot_id, res = reservation, curtime=datetime.now())

@user_routes.route("/confirmreleasespot/<int:user_id>/<int:spot_id>")
def confirmreleasespot(user_id, spot_id):
    #check who is releasing spot
    spot = Spots.query.filter_by(spot_id = spot_id).first()
    reserved = Reservations.query.filter_by(spot_id = spot_id, leaving_timestamp=None).first()
    if spot.status==Status.O:
        spot.status = Status.A
    else:
        return "ERROR spot status user_routes"
    if reserved.leaving_timestamp==None:
        reserved.leaving_timestamp = datetime.now()
    else:
        return "ERROR leaving timestamp user_routes"
    db.session.commit()
    return redirect(url_for("user_routes.home",user_id = session["user_id"]))

@user_routes.route("/bookspot/<int:user_id>")
def bookspot(user_id):
    user = Users.query.filter_by(user_id = user_id).first()
    search = request.args.get("location")
    if search:
        lots = Lots.query.filter(Lots.location.ilike(f"%{search}%")).all()
        return render_template("user_reserve.html", user = user, lots = lots, search = search)
    else:
        return render_template("user_reserve.html", user = user, lots = None)

@user_routes.route("/reservespot/<int:user_id>/<int:lot_id>", methods = ["GET", "POST"])
def reservespot(user_id, lot_id):
    user = Users.query.filter_by(user_id = user_id).first()
    lot = Lots.query.filter_by(lot_id = lot_id).first()
    if request.method=="POST":
        available = [i for i in lot.spots if i.status==Status.A]
        if len(available)<=0:
            return "lot empty"
        spot = available[0]
        if spot.status==Status.A:
            spot.status = Status.O
        else:
            return "invalid status"
        res=Reservations(
            spot_id = spot.spot_id,
            user_id = user_id,
            parking_timestamp = datetime.now(),
            leaving_timestamp = None,
            price_per_hour = lot.price,
            vehicle_number = request.form.get("vehicle")
        )
        db.session.add(res)
        db.session.commit()
        return redirect(url_for("user_routes.home", user_id=user_id))

    return render_template("user_reserve_confirm.html",user = user, lot = lot)

@user_routes.route("/summary/<int:user_id>")
def summary(user_id):
    user = Users.query.filter_by(user_id = user_id).first()
    query = text(
        f"""
        SELECT l.location, count(*) AS total
        FROM lots l 
        JOIN spots s ON (s.lot_id = l.lot_id)
        JOIN reservations r ON (r.spot_id = s.spot_id)
        JOIN users u ON (u.user_id = r.user_id)
        WHERE u.user_id = {user_id}
        GROUP BY l.location"""
    )
    res = db.session.execute(query)
    data1 = {}

    for row in res:
        data1[row.location] = row.total

    return render_template("user_summary.html", user = user, data1 = data1)

@user_routes.route('/useredit/<int:user_id>', methods = ["GET","POST"])
def useredit(user_id):
    user = Users.query.filter_by(user_id = user_id).first()
    if request.method=="POST":
        password = request.form.get("password")
        fullname = request.form.get("fullname")
        address = request.form.get("address")
        pincode = request.form.get("pincode")

        if len(password)<8 or len(password)>32:
            return render_template("user_edit.html", user=user, hide_alert = False, bad_alert=True, alert_text = "Password length should be between 8 and 32")
        elif len(fullname)==0:
            return render_template("user_edit.html", user=user, hide_alert = False, bad_alert=True, alert_text = "Full name cannot be empty")
        elif len(address)==0:
            return render_template("user_edit.html", user=user, hide_alert = False, bad_alert=True, alert_text = "Address cannot be empty")
        elif len(pincode)==0:
            return render_template("user_edit.html", user=user, hide_alert = False, bad_alert=True, alert_text = "Pincode cannot be empty")        
        else:
            user.passw = password
            user.name  = fullname
            user.address=address
            user.pincode=pincode
            db.session.commit()
            return render_template("user_edit.html", user=user, hide_alert = False, bad_alert=False, alert_text = "Updated Successfully")        
        
    return render_template("user_edit.html", user=user, hide_alert=True)

