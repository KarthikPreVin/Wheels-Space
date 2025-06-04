from flask import Flask,render_template,request,jsonify,redirect,url_for,session
from controllers import auth_RBAC

app = Flask(__name__)
app.register_blueprint(auth_RBAC.auth_rbac)

@app.route("/")
def main():
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)
