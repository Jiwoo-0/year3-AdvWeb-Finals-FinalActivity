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
    pirates = Pirates.getAllByUser({"pirate_user_id": session['user_id']})

    return render_template("dashboard.html", pirates=pirates, logged_user=logged_user)

@app.route("/pirate/new")
def AddPirate():
    if 'user_id' not in session:
        return redirect(url_for("index"))
    
    logged_user = Users.getOne({"id": session['user_id']})

    return render_template("newPirate.html", logged_user=logged_user)

@app.route("/pirate/create", methods=["POST"])
def AddPirateProcess():
    if 'user_id' not in session:
        return redirect(url_for("index"))
    
    data = {
        "pirate_name": request.form["pirate_name"],
        "pirate_img": request.form["pirate_img"],
        "pirate_chest": request.form["pirate_chest"],
        "pirate_phrase": request.form["pirate_phrase"],
        "pirate_position": request.form["pirate_position"],
        "pirate_hasPegleg": 1 if "pirate_hasPegleg" in request.form else 0,
        "pirate_hasEyepatch": 1 if "pirate_hasEyepatch" in request.form else 0,
        "pirate_hasHackhand": 1 if "pirate_hasHackhand" in request.form else 0,
        "pirate_user_id": session['user_id']
    }

    print("Pirate has peg leg", data['pirate_hasPegleg'])
    print("Pirate has eye patch", data['pirate_hasEyepatch'])
    print("Pirate has hack hand", data['pirate_hasHackhand'])
    
    if len(data["pirate_name"]) < 2:
        return render_template("newPirate.html", error="Pirate name must be at least 2 characters long.")

    Pirates.new_pirate(data)
    return redirect(url_for("AddPirate"))

@app.route("/pirate/delete/<id>")
def delete_pirate(id):
    if 'user_id' not in session:
        return redirect(url_for("index"))
    
    Pirates.delete_pirate({"id": id})
    return redirect(url_for("dashboard"))

@app.route("/pirate/<id>")
def about_pirate(id):
    if 'user_id' not in session:
        return redirect(url_for("index"))
    
    logged_user = Users.getOne({"id": session['user_id']})
    pirate = Pirates.getOne({"id": id})

    if not pirate:
        return redirect(url_for("dashboard"))

    return render_template("aboutPirate.html", pirate=pirate, logged_user=logged_user)

@app.route("/pirate/update/leg/<id>")
def update_pirate_leg(id):
    if 'user_id' not in session:
        return redirect(url_for("index"))
    
    pirate = Pirates.getOne({"id": id})

    if pirate.pirate_hasPegleg == 1:
        pirate.pirate_hasPegleg = 0
    else:
        pirate.pirate_hasPegleg = 1
    
    Pirates.update_pirate({
        "id": id,
        "pirate_name": pirate.pirate_name,
        "pirate_img": pirate.pirate_img,
        "pirate_chest": pirate.pirate_chest,
        "pirate_phrase": pirate.pirate_phrase,
        "pirate_position": pirate.pirate_position,
        "pirate_hasPegleg": pirate.pirate_hasPegleg,
        "pirate_hasEyepatch": pirate.pirate_hasEyepatch,
        "pirate_hasHackhand": pirate.pirate_hasHackhand,
        "pirate_user_id": pirate.pirate_user_id
    })

    return redirect(url_for("about_pirate", id=id))

@app.route("/pirate/update/eye/<id>")
def update_pirate_eye(id):
    if 'user_id' not in session:
        return redirect(url_for("index"))
    
    pirate = Pirates.getOne({"id": id})

    if pirate.pirate_hasEyepatch == 1:
        pirate.pirate_hasEyepatch = 0
    else:
        pirate.pirate_hasEyepatch = 1
    
    Pirates.update_pirate({
        "id": id,
        "pirate_name": pirate.pirate_name,
        "pirate_img": pirate.pirate_img,
        "pirate_chest": pirate.pirate_chest,
        "pirate_phrase": pirate.pirate_phrase,
        "pirate_position": pirate.pirate_position,
        "pirate_hasPegleg": pirate.pirate_hasPegleg,
        "pirate_hasEyepatch": pirate.pirate_hasEyepatch,
        "pirate_hasHackhand": pirate.pirate_hasHackhand,
        "pirate_user_id": pirate.pirate_user_id
    })

    return redirect(url_for("about_pirate", id=id))

@app.route("/pirate/update/hand/<id>")
def update_pirate_hand(id):
    if 'user_id' not in session:
        return redirect(url_for("index"))
    
    pirate = Pirates.getOne({"id": id})

    if pirate.pirate_hasHackhand == 1:
        pirate.pirate_hasHackhand = 0
    else:
        pirate.pirate_hasHackhand = 1
    
    Pirates.update_pirate({
        "id": id,
        "pirate_name": pirate.pirate_name,
        "pirate_img": pirate.pirate_img,
        "pirate_chest": pirate.pirate_chest,
        "pirate_phrase": pirate.pirate_phrase,
        "pirate_position": pirate.pirate_position,
        "pirate_hasPegleg": pirate.pirate_hasPegleg,
        "pirate_hasEyepatch": pirate.pirate_hasEyepatch,
        "pirate_hasHackhand": pirate.pirate_hasHackhand,
        "pirate_user_id": pirate.pirate_user_id
    })

    return redirect(url_for("about_pirate", id=id))

if __name__ == "__main__":
    app.run(debug=True)