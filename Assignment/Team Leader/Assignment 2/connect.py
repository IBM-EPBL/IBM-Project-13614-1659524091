import ibm_db

def list_all():
    sql = "SELECT * from userlogin"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary !=False:
       
        print ("The Email is: ", dictionary["EMAIL"])
        print ("The Username is: \n", dictionary["USERNAME"])
        print ("The Register No. is: \n", dictionary["REGNO"])
        print ("The Password is: \n", dictionary["PASSWORD"])
       
        dictionary = ibm_db.fetch_both(stmt)

def insert_values(email, username, regno, password, ):
    sql = "INSERT INTO userlogin VALUES('{}','{}','{}','{}')".format(email, username, regno, password)
    stmt = ibm_db.exec_immediate(conn,sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate:DigiCertGlobalRootCA;PROTOCOL=TCPIP;UID=zky66849;PWD=PD99bv4PFtfXhO77;", "", "")
    print("DB is success")
    # insert_values("123@gmail.com","albert123","88475","albert@123")
    # list_all()
 
except:
    print("Connection failed")


