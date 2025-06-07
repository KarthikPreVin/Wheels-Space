from flask import Blueprint, request, render_template

auth_rbac = Blueprint("auth_rbac",__name__)

@auth_rbac.route("/submitlogin", methods=["POST", "GET"])
def submitlogin():
    if request.method =="POST":
        email = request.form["email"]
        password = request.form["password"]
        print(email,password)
        if email == "admin@123":
            return render_template("admin_login.html")
        else:
            return render_template("user_login.html")

    else:
        print("GET REQUEST FROM LOGIN FORM UNEXPECTED BEHAVIOUR")
        return render_template("error_page.html",error_title="Unexpected Page Behaviour",error_text="GET REQUEST FROM LOGIN FORM UNEXPECTED BEHAVIOUR")
    
@auth_rbac.route("/signup")
def signup():
    return render_template("signup.html")

@auth_rbac.route("/createaccount", methods = ["GET","POST"])
def createnew():
    return render_template("user_login.html")