from flask import Blueprint, session, url_for, render_template, redirect, request
from sqlalchemy.orm import joinedload
from models import *
from mydb import db
from sqlalchemy import text
from datetime import datetime

admin_routes = Blueprint("admin_routes",__name__)



@admin_routes.route("/adminhome")
def adminhome():
    if session.get("role")!="ADMIN":
        return "INVALID PAGE REQUEST"
    
    lots_join_spots: list[Lots] = Lots.query.options(joinedload(Lots.spots)).all()
    return render_template("admin_login.html", all_lots=lots_join_spots)

@admin_routes.route("/editlot/<int:lot_id>", methods=["GET", "POST"])
def editlot(lot_id):
    lot = Lots.query.filter_by(lot_id=lot_id).first()
    if lot==None:
        return "ERROR editlot lot not found!"
    
    if request.method == "POST":
        lot_loc = request.form.get("location")
        lot_address = request.form.get("address")
        pincode = request.form.get("pincode")
        rate = request.form.get("rate-per-hour")
        max_spots = request.form.get("max-spots")

        if lot_loc=="":
            return render_template("admin_edit_lot.html",lot = lot, bad_alert=True, hide_alert=False, alert_text="Location cannot be empty")
        if pincode=="":
            return render_template("admin_edit_lot.html",lot = lot, bad_alert=True, hide_alert=False, alert_text="Pincode cannot be empty")
        if lot_address=="":
            return render_template("admin_edit_lot.html",lot = lot, bad_alert=True, hide_alert=False, alert_text="Address cannot be empty")
        if rate=="":
            return render_template("admin_edit_lot.html",lot = lot, bad_alert=True, hide_alert=False, alert_text="Rate per hour cannot be empty")
        if max_spots=="":
            return render_template("admin_edit_lot.html",lot = lot, bad_alert=True, hide_alert=False, alert_text="Max spots cannot be empty")

        if int(max_spots)<lot.max_spots:
            return render_template("admin_edit_lot.html",lot = lot, bad_alert=True, hide_alert=False, alert_text = "Cannot reduce max spots. manually delete spots individually")
        if float(rate)<0:
            return render_template("admin_edit_lot.html",lot = lot, bad_alert=True, hide_alert=False, alert_text="Rate per hour must be positive")
        
        lot.location = lot_loc
        lot.address = lot_address
        lot.pincode = int(pincode)
        lot.rate = float(rate)
        for i in range(int(max_spots)-lot.max_spots):
            new_spot = Spots(
                lot_id = lot.lot_id,
                status = Status.A
            )
            db.session.add(new_spot)
        lot.max_spots = int(max_spots)
        db.session.commit()
        return render_template("admin_edit_lot.html",lot = lot, bad_alert=False, hide_alert=False, alert_text="LOT UPDATION SUCCESS")
        
    else:
        return render_template("admin_edit_lot.html",lot = lot, hide_alert=True)

@admin_routes.route("/deletelot/<int:lot_id>")
def deletelot(lot_id):
    lot = Lots.query.filter_by(lot_id=lot_id).first()
    
    for spot in lot.spots:
        if spot.status==Status.O:
            return render_template("admin_delete_lot.html",lot = lot, flag = 1)
    
    return render_template("admin_delete_lot.html",lot = lot, flag = 0)

@admin_routes.route("/processdelete/<int:lot_id>")
def processdelete(lot_id):
    lot = Lots.query.filter_by(lot_id = lot_id).first()
    for spot in lot.spots:
        for res in spot.reservation:
            res.spot_id = None
        db.session.delete(spot)
    db.session.delete(lot)
    db.session.commit()
    return redirect(url_for("admin_routes.adminhome"))

@admin_routes.route("/viewspot/<int:spot_id>")
def viewspot(spot_id):
    spot = Spots.query.filter_by(spot_id=spot_id).first()
    if spot.status==Status.O:
        reservation = Reservations.query.filter_by(spot_id=spot_id,leaving_timestamp=None).first()
    else:
        reservation = None
    return render_template("admin_view_spot.html", spot=spot, reservation=reservation)

@admin_routes.route("/deletespot/<int:spot_id>")
def deletespot(spot_id):
    spot = Spots.query.filter_by(spot_id=spot_id).first()
    lot = Lots.query.filter_by(lot_id = spot.lot_id).first()
    for res in spot.reservation:
        res.spot_id = None
    lot.max_spots-=1
    db.session.delete(spot)
    db.session.commit()
    return redirect(url_for("admin_routes.adminhome"))

@admin_routes.route("/addlot", methods=["GET", "POST"])
def addlot():
    if request.method=='POST':
        lot_loc = request.form.get("location")
        lot_address = request.form.get("address")
        pincode = request.form.get("pincode")
        rate = request.form.get("rate-per-hour")
        max_spots = request.form.get("max-spots")

        if lot_loc=="":
            return render_template("admin_add_lot.html", bad_alert=True, hide_alert=False, alert_text="Location cannot be empty")
        if pincode=="":
            return render_template("admin_add_lot.html", bad_alert=True, hide_alert=False, alert_text="Pincode cannot be empty")
        if lot_address=="":
            return render_template("admin_add_lot.html", bad_alert=True, hide_alert=False, alert_text="Address cannot be empty")
        if rate=="":
            return render_template("admin_add_lot.html", bad_alert=True, hide_alert=False, alert_text="Rate per hour cannot be empty")
        if max_spots=="":
            return render_template("admin_add_lot.html", bad_alert=True, hide_alert=False, alert_text="Max spots cannot be empty")

        if int(max_spots)<0:
            return render_template("admin_add_lot.html", bad_alert=True, hide_alert=False, alert_text = "Max Spots must be positive")
        
        if float(rate)<0:
            return render_template("admin_add_lot.html", bad_alert=True, hide_alert=False, alert_text="Rate per hour must be positive")
        
        lot = Lots(
            location = lot_loc,
            address = lot_address,
            pincode = int(pincode),
            price = float(rate),
            max_spots = int(max_spots)
            )
        db.session.add(lot)
        db.session.commit()
        for i in range(int(max_spots)):
            new_spot = Spots(
                lot_id = lot.lot_id,
                status = Status.A
            )
            db.session.add(new_spot)
        db.session.commit()
        return render_template("admin_add_lot.html", hide_alert = False, bad_alert = False, alert_text = "LOT CREATED SUCCESSFULLY")
    else:
        return render_template("admin_add_lot.html", hide_alert = True)

@admin_routes.route("/adminusers")
def adminusers():
    users = Users.query.all()
    return render_template("admin_users.html", all_users = users[1:])

@admin_routes.route("/adminhistory")
def adminhistory():
    uid = request.args.get("userid")
    if (uid!=None):
        if not uid.isdigit():
            return render_template("admin_history.html", search=False)
        else:
            user = Users.query.filter_by(user_id = uid).first()
            if user==None:
                return render_template("admin_history.html",search=False,show_alert=True)
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
                                WHERE users.user_id = {uid};""")
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

            return render_template("admin_history.html", search=True, user_id = uid, reservations = res, datetime=datetime)
    else:
        return render_template("admin_history.html", search=False)

@admin_routes.route("/adminsearch")
def adminsearch():
    return render_template("admin_search.html")

@admin_routes.route("/adminsummary")
def adminsummary():
    return render_template("admin_summary.html")

@admin_routes.route("/adminedit", methods = ["GET","POST"])
def adminedit():
    user = Users.query.filter_by(user_id = 1).first()
    if request.method=="POST":
        password = request.form.get("password")
        fullname = request.form.get("fullname")
        address = request.form.get("address")
        pincode = request.form.get("pincode")

        if len(password)<8 or len(password)>32:
            return render_template("admin_edit.html", user=user, hide_alert = False, bad_alert=True, alert_text = "Password length should be between 8 and 32")
        elif len(fullname)==0:
            return render_template("admin_edit.html", user=user, hide_alert = False, bad_alert=True, alert_text = "Full name cannot be empty")
        elif len(address)==0:
            return render_template("admin_edit.html", user=user, hide_alert = False, bad_alert=True, alert_text = "Address cannot be empty")
        elif len(pincode)==0:
            return render_template("admin_edit.html", user=user, hide_alert = False, bad_alert=True, alert_text = "Pincode cannot be empty")        
        else:
            user.passw = password
            user.name  = fullname
            user.address=address
            user.pincode=pincode
            db.session.commit()
            return render_template("admin_edit.html", user=user, hide_alert = False, bad_alert=False, alert_text = "Updated Successfully")        
        
    return render_template("admin_edit.html", user=user, hide_alert=True)