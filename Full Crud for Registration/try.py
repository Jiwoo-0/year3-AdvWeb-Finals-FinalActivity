from flask import Flask, request, render_template, redirect
app = Flask("__name__")
from customers import Customer


@app.route("/")
def index():
    currentList = Customer.getall_customers()
    return render_template("index.html", currentList = currentList, error = "")


@app.route("/process/new", methods=['POST'])
def createNew():
    data={
        "customer_firstname": request.form['customer_firstname'],
        "customer_lastname": request.form['customer_lastname'],
        "customer_email": request.form['customer_email'],
        "customer_age": request.form['customer_age']
    }
    
    if len(data["customer_email"]) < 2 or len(data["customer_email"]) > 16:
        return render_template('index.html', error = "Email is too long or too short")
    
    if int(data["customer_age"]) < 15:
        return render_template('index.html', error = "Age is too young to register")
    
    
    Customer.new_customer(data)
    return redirect("/")

@app.route("/delete/<id>")
def delete(id):
    id = {"id": id}
    Customer.delete_customer(id)
    return redirect("/")
    

if __name__ == "__main__":
    app.run(debug=True)