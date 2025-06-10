from flask import Blueprint, session, url_for, render_template, redirect, request

from models import *
from mydb import db

admin_routes = Blueprint("admin_routes",__name__)

@admin_routes.route("/adminhome")
def adminhome():
    return render_template("admin_login.html")



@admin_routes.route("/adminusers")
def adminusers():
    return render_template("admin_users.html")

@admin_routes.route("/adminsearch")
def adminsearch():
    return render_template("admin_search.html")

@admin_routes.route("/adminsummary")
def adminsummary():
    return render_template("admin_summary.html")

@admin_routes.route("/adminedit")
def adminedit():
    return render_template("admin_edit.html")