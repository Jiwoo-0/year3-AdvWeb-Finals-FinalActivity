from flask import Flask, render_template, request, redirect, url_for
from flask import session
from user_tbl import Users
from pirate_tbl import Pirates

app = Flask(__name__)
app.secret_key = "rolbox"

@app.route("/")
def index():
    return render_template("index.html", error="", log_error="")

@app.route("/register/process", methods=["POST"])
def register_process():
    data = {
        "user_firstname": request.form["user_firstname"],
        "user_lastname": request.form["user_lastname"],
        "user_email": request.form["user_email"],
        "user_password": request.form["user_password"]
    }
    
    if(len(data["user_firstname"])<2):
        return render_template("index.html", error="First name must be at least 2 characters long.")
    
    if(len(data["user_lastname"])<2):
        return render_template("index.html", error="Last name must be at least 2 characters long.")
    
    if(len(data["user_email"])<2 or data["user_email"].__contains__(" ")):
        return render_template("index.html", error="Email must be at least 2 characters long and cannot contain spaces.")
        
    if(data["user_password"] != request.form["repw"]):
        return render_template("index.html", error="Passwords do not match.")
    
    Users.new_user(data)
    return redirect(url_for("index"))

@app.route("/login/process", methods=["POST"])
def login_process():
    email = request.form["user_email"]
    password = request.form["user_password"]
    
    if not email or not password:
        return render_template("index.html", log_error="Email and password cannot be empty.")
    
    user = Users.FindByEmail({"user_email": email})

    if not user or user.user_password != password:
        return render_template("index.html", log_error="Invalid Email and Password")
    
    session['user_id'] = user.id
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/pirates")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for("index"))
    
    logged_user = Users.getOne({"id": session['user_id']})
    return render_template("dashboard.html")

@app.route("/pirate/new")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for("index"))
    
    logged_user = Users.getOne({"id": session['user_id']})

    return render_template("newPirate.html")


if __name__ == "__main__":
    app.run(debug=True)