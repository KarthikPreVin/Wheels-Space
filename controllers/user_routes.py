from flask import Blueprint, session, url_for, render_template, redirect, request

from models import *
from mydb import db
from sqlalchemy import text


user_routes = Blueprint("user_routes",__name__)

@user_routes.route("/home/<int:user_id>")
def home(user_id):
    user = Users.query.filter_by(user_id = user_id).first()
    raw_sql =  text(f"""SELECT 
                            lots.lot_id, 
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
    # print(res)
    # for i in res[0]:
    #     print(i, type(i))
    # returns: [(1, 'Adambakkam 2', 'AB01 DE0124', '2025-06-12 19:43:18.681450', None), (2, 'Location2', 'AB0 BC1024', '2025-06-12 19:43:18.681450', None)]
    # 1 <class 'int'>
    # Adambakkam 2 <class 'str'>
    # AB01 DE0124 <class 'str'>
    # 2025-06-12 19:43:18.681450 <class 'str'>
    # None <class 'NoneType'>
    # print(res[0].lot_id, res[0].location, res[0].vehicle_number, res[0].parking_timestamp, )
    print(type(res[0]))
    return render_template("user_login.html", user = user, reservations = res)

@user_routes.route("/summary/<int:user_id>")
def summary(user_id):
    user = Users.query.filter_by(user_id = user_id).first()
    return render_template("user_summary.html", user = user)

@user_routes.route('/useredit/<int:user_id>')
def useredit(user_id):
    user = Users.query.filter_by(user_id = user_id).first()
    return render_template("user_edit.html", user = user)

