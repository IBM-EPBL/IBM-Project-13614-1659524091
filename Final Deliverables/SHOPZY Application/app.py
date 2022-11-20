import datetime
from datetime import datetime
import email
from pickletools import read_unicodestring1
from turtle import st, update
import ibm_db
from flask import Flask, flash, render_template, request, session, url_for, redirect
from flask_mail import Mail, Message
from flask import *

# This is to get the database access from connect.py code
import connect

app = Flask(__name__)
app.secret_key = 'your secret key'
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'team06inventory@gmail.com'

app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# itemData={"id":pid,"name":pname,"quantity":quantity,"price":price,"minquantity":minquan}

@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/login.html")
def loginpage():
    return render_template("login.html")

@app.route("/adminlogin.html", methods = ['GET','POST'])
def adminlogin():
    return render_template("adminlogin.html")   

@app.route('/admindata', methods=['POST', 'GET'])
def admin():
    # userdatabase = []
    if request.method == 'POST':
        email = request.form.get('adminemail')
        password = request.form.get('adminpassword')

        sql = "SELECT * FROM ADMIN WHERE EMAIL = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(connect.conn,sql)

        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            return render_template("admin/index.html")
    return render_template("adminlogin.html")

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
    return render_template("login.html")

@app.route("/register.html")
def register():
    return render_template("register.html")

@app.route("/registerdata", methods=['GET','POST'])
def registernew():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['pwd']
        mobile = request.form['ph']

        sql = "SELECT * FROM SHOP WHERE EMAIL = ?"
        stmt = ibm_db.prepare(connect.conn,sql)
        ibm_db.bind_param(stmt,1,email)
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

@app.route('/index.html')
def front():
    return render_template("index.html")

@app.route("/products.html")
def dashboard():
    return render_template("products.html")

@app.route("/addproducts.html")
def addprod():
    return render_template("addproducts.html")


@app.route("/addproducts.html",methods = ['POST', 'GET'])
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


# @app.route('/productlist')
# def productlist():
#   if request.method == 'POST':
#         pname = request.form['pname']
#   if session['loggedin'] == True:
#     products = []
#     sql = "SELECT * FROM LIST WHERE PRODUCTNAME = ?"
#     prep_stmt = ibm_db.prepare(connect.conn, sql)
#     ibm_db.bind_param(prep_stmt, 1,pname)
#     ibm_db.execute(prep_stmt)
#     dictionary = ibm_db.fetch_assoc(prep_stmt)
#     while dictionary != False:
#       # print ("The Name is : ",  dictionary)
#       products.append(dictionary)
#       dictionary = ibm_db.fetch_both(prep_stmt)

#     if products:
#       return render_template("list.html", products = products , session = session)
#     else:
#       return render_template("list.html")
#   else:
#     return redirect(url_for('home'))



@app.route('/contact.html')
def contact():
    return render_template("contact.html")

@app.route('/complaint.html')
def compalint():
    return render_template("complaint.html")

@app.route("/complaintdata", methods=['POST', 'GET'])
def complaintdata():
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        complaint =  request.form['complaint']
        sql = "INSERT INTO COMPLAINT (NAME,MAIL,COMPLAINT) VALUES (?,?,?);"
        prep_stmt = ibm_db.prepare(connect.conn, sql)
        ibm_db.bind_param(prep_stmt, 1, name)
        ibm_db.bind_param(prep_stmt, 2, mail)
        ibm_db.bind_param(prep_stmt, 3, complaint)
        ibm_db.execute(prep_stmt)
        # flash("Complaint Sent", "Thank you for contacting us.")
        return render_template('complaint.html', msg = "Complaint Sent. Thank you for contacting us.") 
    return render_template("complaint.html")


# For Admin
@app.route("/updateproducts.html")
def updateprod():
    return render_template("admin/updateproducts.html")


@app.route('/list.html')
def list():
    return render_template("list.html")




@app.route('/contactsupport')
def contactsupport():
  if session['loggedin'] == True:
    return render_template('dashboard/contactsupport.html')
  else:
    return redirect(url_for('home'))

@app.route("/updateproducts",methods = ['POST', 'GET'])
def updateproducts():
    if request.method == 'POST':
        pid = request.form['pid']
        pname = request.form['pname']
        quantity = request.form['quantity']
        minquan = request.form['minquan']
        price =  request.form['price']
        

        sql = "SELECT * FROM INVENTORY WHERE NAME =?"
        prep_stmt = ibm_db.prepare(connect.conn, sql)
        ibm_db.bind_param(prep_stmt,1,pname)
        ibm_db.execute(prep_stmt)
        product = ibm_db.fetch_assoc(prep_stmt)
        itemData={"id":pid,"name":pname,"quantity":quantity,"price":price,"minquantity":minquan}
        if product:

          if product['NAME']==pname:
            
            return render_template('admin/updateproducts.html', msg="Product already existed! Add a new product.") 
        
        
        else: 
            sql ="INSERT INTO INVENTORY (ID,NAME,QUANTITY,MINQUANTITY,PRICE) VALUES (?,?,?,?,?);"
            prep_stmt = ibm_db.prepare(connect.conn, sql)
            ibm_db.bind_param(prep_stmt,1,itemData["id"])
            ibm_db.bind_param(prep_stmt,2,itemData["name"])
            ibm_db.bind_param(prep_stmt,3,itemData["quantity"])
            ibm_db.bind_param(prep_stmt,5,itemData["minquantity"])
            ibm_db.bind_param(prep_stmt,4,itemData["price"])
            
            ibm_db.execute(prep_stmt)
            return render_template('admin/updateproducts.html', msg="Product added")
    sql = "SELECT * FROM INVENTORY WHERE MINQUANTITY <= QUANTITY"
     
       
    stmt = ibm_db.prepare(connect.conn,sql)
    ibm_db.execute(stmt)
    data = ibm_db.fetch_assoc(stmt)

    alertMsg='Following products are to be placed \n'
    if itemData["minquantity"]<=itemData["quantity"]:
        mesg = Message(
                'Hello',
                sender ='team06inventory@gmail.com',
                recipients = [email]
               )
        mesg.body = data
        mail.send(mesg)
        msg = "The following items need to be purchaswed for next day!!\nl"
    return render_template("admin/updateproducts.html")

# scheduler = BlockingScheduler()
# @scheduler.scheduled_job(IntervalTrigger(hours=3))
# def train_model():
    
# scheduler.start()
    


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    session.pop('name', None)
    return render_template("home.html")




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

