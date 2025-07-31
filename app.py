from flask import Flask,render_template
from controllers import *
from models import *
from mydb import db
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = secrets.token_hex(16)
app.register_blueprint(auth_RBAC.auth_rbac)
app.register_blueprint(admin_routes.admin_routes)
app.register_blueprint(user_routes.user_routes)

db.init_app(app)
with app.app_context():
    db.create_all()
    check = Users.query.filter_by(email="admin@123")
    if check.count()==0:
        admin = Users(email = "admin@123", passw = "admin", name="ADMIN", address = "nil", pincode = 0)
        db.session.add(admin)
        db.session.commit()

@app.route("/")
def main():
    return render_template("index.html")

if __name__=="__main__":
    app.run(host="0.0.0.0")
