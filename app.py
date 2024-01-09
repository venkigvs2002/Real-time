from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mail import *
import pandas as pd
from flask_socketio import SocketIO, emit
import secrets
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug.utils import secure_filename
import mysql.connector
import plotly.express as px
from PIL import Image
import plotly.express as px




mydb = mysql.connector.connect(host="localhost",user="root",passwd="",database="epidemic",charset='utf8',port=3306)
mycursor = mydb.cursor()

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
socketio = SocketIO(app)

#home page
@app.route('/')
def index():
    return render_template('index.html')

#doctor login page
@app.route("/doctorlog", methods=["POST", "GET"])
def doctorlog():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        sql = "select * from doctor where email='%s' and password='%s'" % (email, password)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        
        if len(results) > 0:
            session['docemail'] = email
            print(session['docemail'])
            return render_template('doctorhome.html', msg="Login successfull")
        else:
            return render_template('doctorlog.html', msg="Login failed")
    return render_template('doctorlog.html')

#Doctor Registraction page
@app.route("/doctor", methods=["POST", "GET"])
def doctor():
    profilepath = ""  # Initialize profilepath with a default value
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password1 = request.form['Con_Password']
        contact = request.form['mobile']
        address = request.form['address']
        myfile = request.files['myfile']
        filename = myfile.filename
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        current_date = datetime.now().date()
        print(current_date)
        print(t)
        if password == password1:
            sql = "select * from doctor where email='%s' and password='%s'" % (email, password)
            mycursor.execute(sql)
            data = mycursor.fetchall()
            print(data)
            if data == []:
                path = os.path.join("static/profiles/", filename)
                myfile.save(path)
                profilepath = "static/profiles/" + filename
                print(name, email, password, address)
                sql = "insert into doctor(name,email,password,contact,address,Date,Time,profile)values(%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (name, email, password, contact, address,current_date,t, profilepath)
                mycursor.execute(sql, val)
                mydb.commit()
                return render_template('doctorlog.html')
            else:
                flash('Details already Exist', "warning")
                return render_template('doctor.html', msg="Details already Exist")
        else:
            flash('password not matched')
            return render_template('doctor.html')
    return render_template('doctor.html')

#forgot password for doctor
@app.route("/forgotpassword",methods=['POST','GET'])
def forgotpassword():
    if request.method=="POST":
        email = request.form['email']
        sql = "select * from doctor where email='%s'"%(email)
        mycursor.execute(sql)
        data = mycursor.fetchall()
        mydb.commit()
        if data !=[]:
            msg ='valid'
            session['sforgotemail'] = email
            return render_template('forgotpassword.html',msg=msg)
        else:
            msg="notvalid"
            flash("Provide Valid Email","warning")
            return render_template('doctorlog.html',msg=msg)
    return render_template('forgotpassword.html',msg='check')

#update password for doctor
@app.route("/updatepassword",methods=['POST','GET'])
def updatepassword():
    if request.method=="POST":
        form = request.form
        email = session['sforgotemail']
        password = form['password']
        confirmpassword =  form['confirmpassword']
        if password == confirmpassword:
            sql = "select * from doctor where email='%s'"%(email)
            mycursor.execute(sql)
            data = mycursor.fetchall()
            mydb.commit()
            if data:
                sql= "update doctor set password='%s' where email='%s'"%(password,session['sforgotemail'])
                mycursor.execute(sql)
                mydb.commit()
                flash("Password Updated Successfully","success")
                return redirect(url_for("doctorlog"))
        else:
             return render_template("doctorlog.html")
         
#doctor home apge
@app.route('/doctorhome')
def doctorhome():
    sql = "select * from doctor where email='" + session['docemail'] + "'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('doctorhome.html', cols=data.columns.values, rows=data.values.tolist())

#patient login page
@app.route("/patientlog", methods=["POST", "GET"])
def patientlog():
    if request.method == "POST":
        pemail = request.form['pemail']
        password = request.form['password']
        sql = "select * from patient where pemail='%s' and password='%s'" % (pemail, password)
        mycursor.execute(sql)
        results = mycursor.fetchall()
        if len(results) > 0:
            session['patiemail'] = pemail
            print(session['patiemail'])
            return render_template('patienthome.html', msg="Login successfull")
        else:
            return render_template('patientlog.html', msg="Login failed")
    return render_template('patientlog.html')

#patinet registration page
@app.route("/patient", methods=["POST", "GET"])
def patient():
    profilepath = ""  # Initialize profilepath with a default value
    if request.method == "POST":
        pname = request.form['pname']
        pemail = request.form['pemail']
        password = request.form['password']
        password1 = request.form['Con_Password']
        pcontact = request.form['pmobile']
        paddress = request.form['paddress']
        myfile = request.files['myfile']
        filename = myfile.filename
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        current_date = datetime.now().date()
        print(current_date)
        print(t)
        if password == password1:
            sql = "select * from patient where pemail='%s' and password='%s'" % (pemail, password)
            mycursor.execute(sql)
            data = mycursor.fetchall()
            print(data)
            if data == []:
                path = os.path.join("static/profiles/", filename)
                myfile.save(path)
                profilepath = "static/profiles/" + filename
                print(pname, pemail, password, paddress)
                sql = "insert into patient(pname,pemail,password,pcontact,paddress,Date,Time,profile)values(%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (pname, pemail, password,pcontact, paddress,current_date,t, profilepath)
                mycursor.execute(sql, val)
                mydb.commit()
                return render_template('patientlog.html')
            else:
                flash('Details already Exist', "warning")
                return render_template('patient.html', msg="Details already Exist")
        else:
            flash('password not matched')
            return render_template('patient.html')
    return render_template('patient.html')

#patinet forgot passowrd page
@app.route("/pforgotpassword",methods=['POST','GET'])
def pforgotpassword():
    if request.method=="POST":
        email = request.form['pemail']
        sql = "select * from patient where pemail='%s'"%(email)
        mycursor.execute(sql)
        data = mycursor.fetchall()
        mydb.commit()
        if data !=[]:
            msg ='valid'
            session['pforgotemail'] = email
            return render_template('pforgotpassword.html',msg=msg)
        else:
            msg="notvalid"
            flash("Provide Valid Email","warning")
            return render_template('patientlog.html',msg=msg)
    return render_template('pforgotpassword.html',msg='check')

#patinet update password page
@app.route("/pupdatepassword",methods=['POST','GET'])
def pupdatepassword():
    if request.method=="POST":
        form = request.form
        email = session['pforgotemail']
        password = form['password']
        confirmpassword =  form['confirmpassword']
        if password == confirmpassword:
            sql = "select * from patient where pemail='%s'"%(email)
            mycursor.execute(sql)
            data = mycursor.fetchall()
            mydb.commit()
            if data:
                sql= "update patient set password='%s' where pemail='%s'"%(password,session['pforgotemail'])
                mycursor.execute(sql)
                mydb.commit()
                flash("Password Updated Successfully","success")
                return redirect(url_for("patientlog"))
        else:
             return render_template("patientlog.html")
         
#patinet home page
@app.route('/patienthome')
def patienthome():
    sql = "select * from patient where pemail='" + session['patiemail'] + "'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('patienthome.html', cols=data.columns.values, rows=data.values.tolist())

#book appintment
@app.route("/bookappintment", methods=["POST", "GET"])
def bookappintment():
    print(id)
    sql = "select * from patient where pemail='" + session['patiemail'] + "'  "
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    pname = dc[0][1]
    pcontact = dc[0][4]
    paddress =dc[0][5]
    profile = dc[0][8]
    pemail = session['patiemail']
    print(pname, pcontact, paddress,profile, pemail)
    return render_template('bookappointment.html', dc=dc)


#nmake appintment
@app.route("/appointment", methods=["POST", "GET"])
def appointment():
    if request.method == "POST":
        id = request.form['id']
        print(id)
        pname = request.form['pname']
        pemail = request.form['pemail']
        pcontact = request.form['pcontact']
        paddress = request.form['paddress']
        profile = request.form['profile']
        dfb = request.form['dfb']
        age = request.form['age']
        fever = request.form['fever']
        Cough = request.form['Cough']
        breathing = request.form['breathing']
        tiredness = request.form['tiredness']
        throat = request.form['throat']
        Runnynose = request.form['Runnynose']
        bodypain = request.form['bodypain']
        Headache = request.form['Headache']
        Vomiting = request.form['Vomiting']
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        current_date = datetime.now().date()
        print(current_date,now,t)
        sql = "insert into bookappointment (pname, pcontact, paddress,profile, pemail,Time, Date,dfb,age,fever,Cough,breathing,tiredness,throat,Runnynose,bodypain,Headache,Vomiting) values(%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s)"
        val = (pname, pcontact, paddress,profile, pemail,t,current_date,dfb,age,fever,Cough,breathing,tiredness,throat,Runnynose,bodypain,Headache,Vomiting)
        data = mycursor.execute(sql, val)
        mydb.commit()
        print(data)
    return redirect(url_for('bookappintment'))

#view appintment
@app.route("/viewappintment")
def viewappintment():
    sql = "select * from bookappointment where status='pending'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewappintment.html', cols=data.columns.values, rows=data.values.tolist())

#accept the requet
@app.route("/aspr/<id>")
def aspr(id=0):
    print(id)
    sql = "select * from bookappointment where status='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    email = dc[0][2]
    password = dc[0][3]
    print(email, password)
    status='Accepted'
    otp="Your File accepted and this is your secret Key :"
    skey = secrets.token_hex(4)
    print("secret key", skey)
    mail_content ='Your request is accepted by Admin and email is:'+ email + ' ' 
    sender_address = 'appcloud887@gmail.com'
    sender_pass = 'uihywuzqiutvfofo'
    receiver_address = email
    # message = MIMEMultipart()
    # message['From'] = sender_address
    # message['To'] = receiver_address
    # message['Subject'] = 'Real Time Mapping Of Epidemic Spread'
    # message.attach(MIMEText(mail_content, 'plain'))
    # session = smtplib.SMTP('smtp.gmail.com', 587)
    # session.starttls()
    # session.login(sender_address, sender_pass)
    # text = message.as_string()
    # session.sendmail(sender_address, receiver_address, text)
    # session.quit()
    sql = "update bookappointment set status='Accepted', EpidemicSpread='Present' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    flash('Doctor Has accepted the request for Patient appointment', 'success')
    return redirect(url_for('viewappintment'))

#reject the requet
@app.route("/reject/<id>")
def reject(id=0):
    print(id)
    sql = "select * from bookappointment where status='pending'"
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    email = dc[0][2]
    password = dc[0][3]
    print(email, password)
    otp="Your File accepted and this is your secret Key :"
    skey = secrets.token_hex(4)
    print("secret key", skey)
    mail_content ='Your request is Rejected by Admin and email is:'+ email + ' ' 
    sender_address = 'appcloud887@gmail.com'
    sender_pass = 'uihywuzqiutvfofo'
    receiver_address = email
    # message = MIMEMultipart()
    # message['From'] = sender_address
    # message['To'] = receiver_address
    # message['Subject'] = 'Real Time Mapping Of Epidemic Spread'
    # message.attach(MIMEText(mail_content, 'plain'))
    # session = smtplib.SMTP('smtp.gmail.com', 587)
    # session.starttls()
    # session.login(sender_address, sender_pass)
    # text = message.as_string()
    # session.sendmail(sender_address, receiver_address, text)
    # session.quit()
    
    sql = "update bookappointment set status='Rejected', EpidemicSpread='Absent' where id='%s'" % (id)
    mycursor.execute(sql)
    mydb.commit()
    flash('Doctor Has Rejected the request for Patient appointment', 'success')
    return redirect(url_for('viewappintment'))

#View appintment status
@app.route("/viewappintmentstatus")
def viewappintmentstatus():
    sql = "select * from bookappointment where status='Accepted'and EpidemicSpread='Present'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewappintmentstatus.html', cols=data.columns.values, rows=data.values.tolist())

#View appintment status by patinet
@app.route("/viewstatus")
def viewstatus():
    sql = "select * from bookappointment where id=id and pemail='" + session['patiemail'] + "'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewstatus.html', cols=data.columns.values, rows=data.values.tolist())

#view payment
@app.route("/viewpayment")
def viewpayment():
    # sql = "select * from bookappointment where id=id and pemail='" + session['patiemail'] + "'"
    # data = pd.read_sql_query(sql, mydb)
    # print(data)
    return render_template('viewpayment.html')

#view payment
@app.route("/viewcardpayment")
def viewcardpayment():
    sql = "select * from payment"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewcardpayment.html',data=data)

#view payment
@app.route("/viewupipayment")
def viewupipayment():
    sql = "select * from upipayment"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('viewupipayment.html',data=data)

#view recovery status
@app.route("/recovery")
def recovery():
    sql = "select * from bookappointment where status='Accepted'and EpidemicSpread='Present' and pemail='" + session['patiemail'] + "'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('recovery.html', cols=data.columns.values, rows=data.values.tolist())

#update recivery
@app.route("/recoverdback/<int:id>")
def recoverdback(id):
    sql = "select * from bookappointment where id=%s"%(id)
    mycursor.execute(sql)
    dc = mycursor.fetchall()
    print(dc)
    pname = dc[0][1]
    pcontact = dc[0][2]
    paddress = dc[0][3]
    profile = dc[0][4]
    pemail = session['patiemail']
    dfb = dc[0][8]
    age = int(dc[0][9])
    fever = dc[0][10]
    Cough = dc[0][11]
    breathing = dc[0][12]
    tiredness = dc[0][13]
    throat = dc[0][14]
    Runnynose= dc[0][15]
    bodypain = dc[0][16]
    Headache  = dc[0][17]
    Vomiting = dc[0][18]
    print(pname, pcontact, paddress,profile, pemail,dfb,age,fever,Cough,breathing,tiredness,throat,Runnynose,bodypain,Headache,Vomiting)
    now = datetime.now()
    t = now.strftime("%H:%M:%S")
    current_date = datetime.now().date()
    print(current_date,now,t)
    sql = "insert into recovery (pname, pcontact, paddress,profile, pemail,Time, Date,dfb,age,fever,Cough,breathing,tiredness,throat,Runnynose,bodypain,Headache,Vomiting) values(%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s,%s)"
    val = (pname, pcontact, paddress,profile, pemail,t,current_date,dfb,age,fever,Cough,breathing,tiredness,throat,Runnynose,bodypain,Headache,Vomiting)
    data = mycursor.execute(sql, val)
    mydb.commit()
    print(data)
    
    sql = "update recovery set EpidemicSpread='Recovered' where id=%s"
    mycursor.execute(sql, (id,))
    mydb.commit()
    return redirect(url_for('recovery'))

@app.route('/paymentback', methods=['POST', 'GET'])
def paymentback():
  
    return render_template('paymentback.html')


#payment 
@app.route('/payment', methods=['POST', 'GET'])
def payment():
    if request.method == 'POST':
        pemail = session['patiemail']
        Amount = request.form['amount']
        Cardname = request.form['cardname']
        Cardnumber = request.form['cardnumber']
        expmonth = request.form['expmonth']
        cvv = request.form['cvv']
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        current_date = datetime.now().date()

        # Check if a record with the same email and date already exists
        check_sql = "SELECT * FROM payment WHERE pemail = %s AND Date = %s"
        check_val = (pemail, current_date)
        mycursor.execute(check_sql, check_val)
        existing_record = mycursor.fetchone()

        if not existing_record:
            # If no existing record, insert the new record
            print(current_date)
            print(t)
            print(pemail, Amount, Cardname, Cardnumber, expmonth, cvv, t, current_date)
            sql = "INSERT INTO payment(pemail, Amount, Cardname, Cardnumber, expmonth, cvv, Date, Time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (pemail, Amount, Cardname, Cardnumber, expmonth, cvv, current_date, t)
            mycursor.execute(sql, val)
            mydb.commit()
    return render_template('payment.html')


#UPI payment 
@app.route('/upipayment', methods=['POST', 'GET'])
def upipayment():
    print("**********************")
    if request.method == 'POST':
        pemail = session['patiemail']
        Amount = request.form['amount']
        UPIID = request.form['upiid']
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        current_date = datetime.now().date()
        print(current_date)
        print(t)
        print(pemail, Amount,UPIID, t, current_date)

        # Check if a record with the same email and date already exists
        check_sql = "SELECT * FROM upipayment WHERE pemail = %s AND Date = %s"
        check_val = (pemail, current_date)
        mycursor.execute(check_sql, check_val)
        existing_record = mycursor.fetchone()

        if not existing_record:
            # If no existing record, insert the new record
            print(current_date)
            print(t)
            print(pemail, Amount,UPIID, t, current_date)
            sql = "INSERT INTO upipayment(pemail, Amount, UPIID,  Date, Time) VALUES (%s, %s, %s, %s, %s)"
            val = (pemail, Amount, UPIID, current_date, t)
            mycursor.execute(sql, val)
            mydb.commit()
    return render_template('upipayment.html')


@app.route('/patientchat', methods=['POST', 'GET'])
def patientchat():
    if request.method == "POST":
        messages = request.form['messages']
        pemail = session['patiemail']
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        current_date = datetime.now().date()
        
        sql = "INSERT INTO chart (messages, email, Date, Time) VALUES (%s, %s, %s, %s)"
        val = (messages, session['patiemail'], current_date, t)
        mycursor.execute(sql, val)
        mydb.commit()

    # Fetch messages from the database
    sql_select = "SELECT * FROM chart WHERE email = %s ORDER BY Date, Time"
    val_select = (session['patiemail'], )
    mycursor.execute(sql_select, val_select)
    messages = mycursor.fetchall()

    return render_template('patientchat.html', messages=messages)
    

# New route for the chat page
@app.route('/doctorchat',  methods=['POST', 'GET'])
def doctorchat():
    email = session['docemail'] 
    pemail =  session['patiemail']
    print(session['docemail'])
   
    if request.method=="POST":
        messages = request.form['messages']
        email = session['docemail']
        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        current_date = datetime.now().date()
        print(current_date)
        print(t)
        print(session['patiemail'])
        sql = "INSERT INTO docchart (messages, email, Date, Time) VALUES (%s, %s, %s, %s)"
        val = (messages,session['docemail'],current_date,t )
        data = mycursor.execute(sql, val)
        print(data)
        mydb.commit()

    # Fetch messages from the database
    sql_select = "SELECT * FROM docchart WHERE email = %s ORDER BY Date, Time"
    val_select = (session['docemail'], )
    mycursor.execute(sql_select, val_select)
    messages = mycursor.fetchall()
    
    return render_template('doctorchat.html', messages=messages)

#view recovery status
@app.route("/recoverystatus")
def recoverystatus():
    sql = "select * from recovery where EpidemicSpread='Recovered'"
    data = pd.read_sql_query(sql, mydb)
    print(data)
    return render_template('recoverystatus.html', cols=data.columns.values, rows=data.values.tolist())

# new route for displaying epidemic details and patient-related graphs
@app.route('/epidemic_details')
def epidemic_details():
    # Fetch data from the database
    sql = "SELECT * FROM bookappointment WHERE EpidemicSpread='Accepted'"
    data = pd.read_sql_query(sql, mydb)

    # Plotting patient-related graphs
    fig1 = px.bar(data, x='Date', y='fever', color='pname', title='Patient Fever Status Over Time')
    fig2 = px.pie(data, names='status', title='Appointment Status Distribution')
    
    # Additional Pie Chart for Symptoms Distribution
    symptoms_columns = ['fever', 'Cough', 'breathing', 'tiredness', 'throat', 'Runnynose', 'bodypain', 'Headache', 'Vomiting']
    symptoms_counts = data[symptoms_columns].apply(lambda x: x.value_counts()).transpose()
    fig3 = px.pie(symptoms_counts, names=symptoms_counts.index, title='Symptoms Distribution Among Patients')

    # Convert figures to HTML for rendering in the template
    graph1_html = fig1.to_html(full_html=False)
    graph2_html = fig2.to_html(full_html=False)
    graph3_html = fig3.to_html(full_html=False)

    return render_template('epidemic_details.html', graph1_html=graph1_html, graph2_html=graph2_html, graph3_html=graph3_html)


if __name__=="__main__":
    app.run(debug=True)