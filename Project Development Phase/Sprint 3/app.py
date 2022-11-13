import datetime
import dbm
from ast import stmt
from datetime import datetime
from multiprocessing import connection
from pickletools import read_unicodestring1
from turtle import st, update

import ibm_db
import pandas as pd
from flask import Flask, render_template, request, session, url_for
from flask_mail import Mail, Message

from mydb import connect

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'team06inventory@gmail.com'
app.config['MAIL_PASSWORD'] = 'pjqnmjtrdlqkjqfj'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def homepage():
    return render_template("login.html")


@app.route("/register.html")
def register():
    return render_template("register.html")

@app.route("/logindata", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        sql = "SELECT * FROM SHOP WHERE EMAIL = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(connect.conn,sql)

        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            return render_template("index.html")
        else:
            return ("Invalid username or password")
    return render_template("/login.html")

@app.route("/registerdata", methods=['GET','POST'])
def registernew():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pwd')
        mobile = request.form.get('ph')
        sql = "SELECT * FROM SHOP WHERE EMAIL = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(connect.conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = "Already existed account! Kindly Login"
            return render_template("login.html")
        else:
            sql = "INSERT INTO SHOP (NAME,EMAIL,PASSWORD,MOBILENUMBER) VALUES('{0}','{1}','{2}','{3}')"
            res = ibm_db.exec_immediate(connect.conn,sql.format(name,email,password,mobile))
            mesg = Message(
                'Hello',
                sender ='team06inventory@gmail.com',
                recipients = [email]
               )
        mesg.body = 'Welcome to Shopzy. Thank you for registering with us.\nHappy Shop(zy)ing!!!.\nLogin id:\n email:'+email+'\nPassword:'+password
        mail.send(mesg)
        msg = "Your account has been registered successfully!l"
        if res:
            return render_template("login.html",msg=msg)

@app.route("/products.html")
def dashboard():
    return render_template("products.html")


@app.route('/addproducts.html',methods = ['POST', 'GET'])
def addproduct():
    if request.method == 'POST':
        pname = request.form['pname']
        quantity = request.form['quantity']
        the_time = datetime.now()
        the_time = the_time.replace(second=0, microsecond=0)
        name =  request.form['name']

        sql = "SELECT * FROM LIST WHERE PRODUCTNAME =?"
        prep_stmt = ibm_db.prepare(connect.conn, sql)
        ibm_db.bind_param(prep_stmt,1,pname)
        ibm_db.execute(prep_stmt)
        product = ibm_db.fetch_assoc(prep_stmt)
        if product:

          if product['PRODUCTNAME']==pname:
            
            return render_template('addproducts.html', msg="Product already added! Add a new product.")
        #   else:
        #     sql ="INSERT INTO LIST (PRODUCTNAME,QUANTITY,DATE,HOLDERNAME) VALUES (?,?,?,?);"
        #     prep_stmt = ibm_db.prepare(connect.conn, sql)
        #     ibm_db.bind_param(prep_stmt, 1, pname)
        #     ibm_db.bind_param(prep_stmt, 2, quantity)
        #     ibm_db.bind_param(prep_stmt, 3, str(the_time))
        #     ibm_db.bind_param(prep_stmt, 4, name)
        #     ibm_db.execute(prep_stmt)
        #     return render_template('addproducts.html', msg="Product added")  
        else: 
            sql ="INSERT INTO LIST (PRODUCTNAME,QUANTITY,DATE,HOLDERNAME) VALUES (?,?,?,?);"
            prep_stmt = ibm_db.prepare(connect.conn, sql)
            ibm_db.bind_param(prep_stmt, 1, pname)
            ibm_db.bind_param(prep_stmt, 2, quantity)
            ibm_db.bind_param(prep_stmt, 3, str(the_time))
            ibm_db.bind_param(prep_stmt, 4, name)
            ibm_db.execute(prep_stmt)
            return render_template('addproducts.html', msg="Product added") 
    return render_template("addproducts.html")



        


if __name__=="__main__":
    app.run(debug = True, port=4996)