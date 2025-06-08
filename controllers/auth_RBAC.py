from flask import Blueprint, request, render_template, session
from models import *
from mydb import db

#add-ons maybe
#### use CSRF (flask-wtf)
#### hash password before storing
#### maybe set constraints for password

auth_rbac = Blueprint("auth_rbac",__name__)

@auth_rbac.route("/login", methods=["POST", "GET"])
def login():
    if request.method =="POST":
        form_email = request.form["email"]
        form_password = request.form["password"]
        result = Users.query.filter_by(email = form_email)
        user = result.first()
        if user!=None:
            if form_email == "admin@123":
                #admin login
                if user.passw == form_password:
                    session["user_id"] = user.user_id
                    session["role"] = "ADMIN"
                    return render_template("admin_login.html")
                else:
                    return render_template("login.html", hide_alert=False, alert_text="Incorrect Password")
            else:
                #user login
                if user.passw == form_password:
                    session["user_id"] = user.user_id
                    session["role"] = "USER"
                    return render_template("user_login.html")
                else:
                    return render_template("login.html", hide_alert=False, alert_text="Incorrect Password")
        else:
            #account doesnt exist
            return render_template("login.html", hide_alert=False, alert_text="!Account doesn't Exist. Create New Account")

    else:
        return render_template("login.html", hide_alert = True)
    
@auth_rbac.route("/signup", methods = ["GET","POST"])
def signup():
    print("SIGNUP ENTERED!!")
    if request.method == "POST":
        form_email = request.form["email"]
        form_password = request.form["password"]
        form_fullname = request.form["fullname"]
        form_address = request.form["address"]
        form_pincode = request.form["pincode"]
        print("EMAIL:" ,form_email)
        check = Users.query.filter_by(email=form_email).first()
        if check!=None:
            #user exists!
            return render_template("signup.html", hide_alert = False, alert_text = "this email is already registered")
        elif len(form_password)<8 or len(form_password)>32:
            return render_template("signup.html", hide_alert = False, alert_text = "Password length should be between 8 and 32")
        elif len(form_fullname)==0:
            return render_template("signup.html", hide_alert = False, alert_text = "Full name cannot be empty")
        elif len(form_address)==0:
            return render_template("signup.html", hide_alert = False, alert_text = "Address cannot be empty")
        elif len(form_pincode)==0:
            return render_template("signup.html", hide_alert = False, alert_text = "Pincode cannot be empty")        
        else:
            #user doesnt exist
            new_user = Users(email = form_email, passw = form_password, name = form_fullname, address = form_address, pincode=form_pincode)#type: ignore
            db.session.add(new_user)
            db.session.commit()
            session["user_id"] = new_user.user_id
            session["role"] = "USER"
            return render_template("user_login.html")
    else:
        return render_template("signup.html", hide_alert = True)
