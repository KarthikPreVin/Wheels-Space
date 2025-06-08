import email
from flask import Flask,render_template,request,jsonify,redirect,url_for,session
from controllers import *
from models import *
from mydb import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.register_blueprint(auth_RBAC.auth_rbac)

db.init_app(app)
with app.app_context():
    db.create_all()
    # from sqlalchemy import inspect
    # print("TABLES: ",inspect(db.engine).get_table_names())
    check = Users.query.filter_by(email="admin@123")
    if check.count()==0:
        admin = Users(email = "admin@123", passw = "admin", name="ADMIN", address = "nil", pincode = 0) #type: ignore
        db.session.add(admin)
        db.session.commit()

@app.route("/")
def main():
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)
