from flask import Flask, render_template, request, redirect, url_for
from user_tbl import Users
from pirate_tbl import Pirates

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", error="")

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
    data={
        "user_email": request.form["user_email"],
        "user_password": request.form["user_password"]
    }
    
    
    
    if(data["user_email"] == "" or data["user_password"] == ""):
        return render_template("index.html", error="Email and password cannot be empty.")
    
    
        
    
    return render_template("dashboard.html")

@app.route("/pirates")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)