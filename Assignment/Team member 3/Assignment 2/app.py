import dbm
from pickletools import read_unicodestring1
from flask import Flask ,render_template, request
import ibm_db
from mydb import connect
app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("register.html")

@app.route("/login.html")
def log():
    return render_template("login.html")

@app.route("/registerdata", methods=['GET','POST']) 
def result():
    print(request.form)
    email = request.form['email']
    username = request.form['username']
    regno = request.form['regno']
    password = request.form['password']
    connect.insert_values(username,email,regno,password)
    return render_template("login.html")


@app.route("/receivedata",methods=['POST'])
def login():
    email = request.form.get('email')
    password=request.form.get('password')
    sql = "SELECT * FROM USERLOGIN WHERE EMAIL = ? AND PASSWORD = ?"
    stmt = ibm_db.prepare(connect.conn,sql)

    ibm_db.bind_param(stmt,1,email)
    ibm_db.bind_param(stmt,2,password)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)

    if account:
        return render_template("welcome.html")
    else:
        return "Invalid Username or Password"    


if __name__=="__main__":
    app.run(debug = True)