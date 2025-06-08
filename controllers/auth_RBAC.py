from flask import Blueprint, request, render_template
from models import *
auth_rbac = Blueprint("auth_rbac",__name__)

@auth_rbac.route("/submitlogin", methods=["POST", "GET"])
def submitlogin():
    if request.method =="POST":
        email_ = request.form["email"]
        password = request.form["password"]
        print(email_,password)
        record = Users.query.filter_by(email = email_)
        if email_ == "admin@123":
            #admin login
            if record.first().passw == password:
                return render_template("admin_login.html")
            else:
                return "wrong password"
        elif record.count()!=0:
            #user login
            if record.first().passw == password:
                return render_template("user_login.html")
            else:
                return "wrong password"
            
        else:
            #account doesnt exist
            pass

    else:
        print("GET REQUEST FROM LOGIN FORM UNEXPECTED BEHAVIOUR")
        return render_template("error_page.html",error_title="Unexpected Page Behaviour",error_text="GET REQUEST FROM LOGIN FORM UNEXPECTED BEHAVIOUR")
    
@auth_rbac.route("/signup")
def signup():
    return render_template("signup.html")

@auth_rbac.route("/createaccount", methods = ["GET","POST"])
def createnew():
    return render_template("user_login.html")