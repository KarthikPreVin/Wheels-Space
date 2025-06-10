from flask import Blueprint, session, url_for, render_template, redirect, request

from models import *
from mydb import db

user_routes = Blueprint("user_routes",__name__)

@user_routes.route("/home")
def home():
    return render_template("user_login.html")

