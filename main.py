from __future__ import unicode_literals
from __future__ import print_function
from colorama import reinit
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, logging
from flaskext.mysql import MySQL
from functools import wraps
from pip import main
from wtforms import Form, StringField, validators
import re
import os
import hashlib 
import bcrypt
import json
import pybase64
import uuid
import user
from flask_mail import Mail, Message
from flask_socketio import SocketIO, emit, send
from flask_cors import CORS
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
CORS(app)
socketio.init_app(app, cors_allowed_origins="*")
users = []



#port = int(os.environ.get('PORT', 5000))

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'canada$God7972#'

# Enter your database connection details below
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD	'] = ''
app.config['MYSQL_DATABASE_DB'] = 'pharmacat'

#app.config['MAIL_SERVER']='smtp.gmail.com'
#app.config['MAIL_PORT'] = 465
#app.config['MAIL_USERNAME'] = 'chalielijalem@gmail.com'
#app.config['MAIL_PASSWORD'] = 'kxtgnwrihqqlszay'
#app.config['MAIL_USE_TLS'] = False
#app.config['MAIL_USE_SSL'] = True

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'bc6dc6dd0fe1c2'
app.config['MAIL_PASSWORD'] = 'c27d7cf4dc2f6f'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False



mail = Mail(app)
# Intialize MySQL
mysql = MySQL(autocommit=True)
mysql.init_app(app)




#Homepage
@app.route('/')
def index():
    return render_template('index.html')


#Dashboard
@app.route('/dashboard')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        if(session['isdoctor']==0):
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            cursor1 = mysql.get_db().cursor()
            records = cursor.execute('SELECT * FROM users')
            return render_template('dashboard.html', account = account, num = records,isdoctor=session['isdoctor'])
        else:
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            cursor1 = mysql.get_db().cursor()
            records = cursor.execute('SELECT * FROM doctors')
            return render_template('doc_dashbord.html', account = account)
        
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/hom')
def hom():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        if(session['isdoctor']==0):
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            cursor1 = mysql.get_db().cursor()
            records = cursor.execute('SELECT * FROM users')
            return render_template('dashboard.html', account = account, num = records,isdoctor=session['isdoctor'])
        else:
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            cursor1 = mysql.get_db().cursor()
            records = cursor.execute('SELECT * FROM doctors')
            return render_template('doc_dashbord.html', account = account)
        
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# doctor dash bord
@app.route('/dochome')
def dochome():
    # Check if user is loggedin
    if session['isdoctor']:
        # User is loggedin show them the home page
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        cursor1 = mysql.get_db().cursor()
        records = cursor.execute('SELECT * FROM doctors')
        return render_template('doc_dashbord.html', account = account, num = records,isdoctor=session['isdoctor'])
    # User is not loggedin redirect to login page
    return redirect(url_for('doclogin'))
    # doctor dash bord

@app.route('/doc_dash')
def doc_dash():
    # Check if user is loggedin
    if session['isdoctor']:
        # User is loggedin show them the home page
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        cursor1 = mysql.get_db().cursor()
        records = cursor1.execute('SELECT * FROM users')
        return render_template('doc_dashbord.html', account = account, num = records,isdoctor=session['isdoctor'])
    # User is not loggedin redirect to login page
    return redirect(url_for('doclogin'))
#Patient Login

@app.route('/admin_dash')
def admin_dash():
    # Check if user is loggedin
    if session['isadmin']:
        # User is loggedin show them the home page
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        cursor = mysql.get_db().cursor()
        records = cursor.execute('SELECT * FROM users')
        return render_template('admin_dashboard.html', account = account, num = records,isadmin=session['isadmin'])
    # User is not loggedin redirect to login page
    return redirect(url_for('adminlogin'))
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE Username = %s', (username))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        # if account:
        if account:
            if bcrypt.checkpw(password.encode('utf-8'), account[2].encode('utf-8')):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['full_name']=account[5]
                session['isdoctor'] = 0
                session['ispatient'] = 1
                x= '1'
                cursor.execute("UPDATE users SET online=%s WHERE ID=%s", (x, account[0]))
                # Redirect to dashboard
                return home()
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect password!'
        else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username'
    # Show the login form with message (if any)
    flash(msg)
    return render_template('patientlogin.html', msg=msg)

#Patient Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        full_name = request.form['full_name']
        address = request.form['address']
        date = request.form['date']
        blood = request.form['blood']
        # Check if account exists using MySQL
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE Username = %s', (username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            apistr = username;
            result = hashlib.md5(apistr.encode()) 
            comb = username+'(~)'+password
            s = comb.encode()
            s1 = pybase64.b64encode(s)
            api=s1.decode('utf-8')
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, NULL, %s, %s, %s, %s, %s,%s, NULL, NULL, NULL, NULL)', (username, hashed_password, email, full_name, address, blood, date, api,0))
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    flash(msg)
    return render_template('patientlogin.html', msg=msg)
#forget password rest option
@app.route('/reset', methods=['GET','POST'])
def reset():
    return render_template('forget.html')
#Doctor Register
@app.route('/docregister', methods=['GET', 'POST'])
def docregister():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        full_name = request.form['full_name']
        registration_number = request.form['registration_number']
        contact_number = request.form['contact_number']
        spec = request.form['specialization']
        address = request.form['address']

        # Check if account exists using MySQL
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM doctors WHERE Username = %s', (username))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            print(username + "\n" + str(hashed_password)+ "\n" + email+ "\n" +full_name+ "\n" +registration_number+ "\n" +contact_number+ "\n" +spec+ "\n" +address)
            cursor.execute('INSERT INTO doctors VALUES (NULL, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s)', ( username, hashed_password, email, full_name, registration_number, contact_number, "" , spec, address ,0))
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    flash(msg)
    return render_template('doctorlogin.html', msg=msg)

#Doctor Login
@app.route('/doclogin', methods=['GET', 'POST'])
def doclogin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM doctors WHERE Username = %s', (username))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        # if account:
        if account:
            if bcrypt.checkpw(password.encode('utf-8'), account[2].encode('utf-8')):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['full_name']= account[4]
                session['isdoctor'] = 1
                x = '1'
                cursor.execute("UPDATE doctors SET online=%s WHERE ID=%s", (x, account[0]))
                # Redirect to home page
                return doc_dash()
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect password!'
        else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username!'
    # Show the login form with message (if any)
    flash(msg)
    return render_template('doctorlogin.html', msg=msg)

#admin login page 
@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', (username))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        # if account:
        if account:
            if bcrypt.checkpw(password.encode('utf-8'), account[2].encode('utf-8')):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['isadmin'] = 1
                # Redirect to home page
                return admin_dash()
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect password!'
        else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username!'
    # Show the login form with message (if any)
    flash(msg)
    return render_template('adminlogin.html', msg=msg)
    
#BMI for the dashboard(Written by Mayank)
@app.route('/bmi',methods=['GET', 'POST'])
def bmi():
    if 'ispatient' in session:
        result=0
        h=0
        w=0
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        if request.method=='POST':
            h=float(request.form["height"])
            h=float(h)
            w=request.form["weight"]
            w=float(w)
            result=w/(h*h)
            result=round(result,2)
        return render_template('bmi.html',ans=result,account=account,height=h,weight=w) 
    else:
        return redirect(url_for('login'))

#av consultancy  
@app.route("/consultation")
def consultation():
    if 'loggedin' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('consultation.html', account=account)
    # User is not loggedin redirect to login page
    else:
        return redirect(url_for('/'))
  
 

#Health Status
@app.route('/healthstatus')
def healthstatus():
    # Check if user is loggedin
    if 'ispatient' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        channel=account[11]
        temp=account[12]
        hum=account[13]
        puls=account[14]
        return render_template('healthstatus.html', account=account,channel=channel, temp=temp, hum=hum, puls=puls)
    # User is not loggedin redirect to login page
    else:
        return redirect(url_for('login'))
#Myaccount Details
@app.route('/myaccount')
def myaccount():
    # Check if user is loggedin
    if 'ispatient' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('myaccount.html', account=account)
    # User is not loggedin redirect to login page
    else:
        return redirect(url_for('login'))

#doctor account Details
@app.route('/docaccount')
def docaccount():
    # Check if user is loggedin
    if 'isdoctor' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        return render_template('docaccount.html', account=account)
    # User is not loggedin redirect to login page
    else:
        return redirect(url_for('doclogin'))
#Book an Appointment 
@app.route('/book',methods=['GET', 'POST'])
def book():
    # Check if user is loggedin
    if 'ispatient' in session:
        
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM doctors")
        appinfo = cur.fetchall()
        
        speci = set()
        for m in appinfo:
            speci.add(m[8])
        
        return render_template('bookhome.html', speci=speci, account=account)
    # User is not loggedin redirect to login page
    else:
        return redirect(url_for('login'))

@app.route('/bookh',methods=['GET', 'POST'])
def bookh():
    # Check if user is loggedin
    if 'ispatient' in session:
        
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM doctors")
        appinfo = cur.fetchall()
        if(request.method == 'POST'):
            fname = request.form['fname']
            session['speci'] = fname
            cursor11 = mysql.get_db().cursor()
            cursor11.execute('SELECT * FROM doctors WHERE Specialization= %s', [fname])
            doc = cursor11.fetchall()
                
            return render_template('book.html', account=account,doc=doc)
        return render_template('bookhome.html', appinfo=appinfo, account=account)
    # User is not loggedin redirect to login page
    else:
        return redirect(url_for('login'))

@app.route('/bookhh',methods=['GET', 'POST'])
def bookhh():
    # Check if user is loggedin
    if 'ispatient' in session:
        
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM doctors")
        appinfo = cur.fetchall()
        if(request.method == 'POST'):
            fname = request.form['fname']
            date = request.form['date']
            time = request.form['time']
            cursor11 = mysql.get_db().cursor()
            cursor11.execute('SELECT * FROM doctors WHERE Full_Name= %s', [fname])
            doc = cursor11.fetchone()
            cursor1 = mysql.get_db().cursor()
            cursor1.execute('INSERT INTO booking VALUES (NULL, %s, %s, %s, %s, %s)', ( doc[0], session['id'], date, time, 0))
            cursor2 = mysql.get_db().cursor()    
            cursor2.execute('SELECT * FROM booking WHERE Patient_ID= %s', [session['id']])
            l = cursor2.fetchall()
            arr = []
            for i in l:
                cursor3 = mysql.get_db().cursor()    
                cursor3.execute('SELECT * FROM doctors WHERE ID= %s', [i[1]])
                doc = cursor3.fetchone()
                arr.append([doc[4],doc[9]])
                
            return render_template('appointments.html', account=account,l=l,arr=arr)
        return render_template('book.html', appinfo=appinfo, account=account)
    # User is not loggedin redirect to login page
    else:
        return redirect(url_for('login'))
#Appointments page for Patients
@app.route('/appointments',methods=['GET', 'POST'])
def appointments():
    # Check if user is loggedin
    if 'ispatient' in session:
        
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        if(account is None):
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            address = account[9]
        else:
            address = account[5]
            
        cursor2 = mysql.get_db().cursor()    
        cursor2.execute('SELECT * FROM booking WHERE Patient_ID= %s', [session['id']])
        l = cursor2.fetchall()
        arr = []
        for i in l:
            cursor3 = mysql.get_db().cursor()    
            cursor3.execute('SELECT * FROM doctors WHERE ID= %s', [i[1]])
            doc = cursor3.fetchone()
            arr.append([doc[4],doc[9]])
            
        return render_template('appointments.html', account=account,l=l,arr=arr)
        # User is not loggedin redirect to login page
    else:
        return redirect(url_for('login'))

@app.route('/curappointment',methods=['GET', 'POST'])
def curappointment():
    # Check if user is loggedin
    if 'isdoctor' in session:
        
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        if(account is None):
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            address = account[5]
        else:
            address = account[9]
            
        cursor2 = mysql.get_db().cursor()    
        cursor2.execute('SELECT * FROM booking WHERE Doctor_ID= %s', [session['id']])
        l = cursor2.fetchall()
        arr = []
        for i in l:
            cursor3 = mysql.get_db().cursor()    
            cursor3.execute('SELECT * FROM users WHERE ID= %s', [i[2]])
            doc = cursor3.fetchone()
            arr.append([doc[5],doc[6]])
            
        return render_template('viewappointments.html', account=account,l=l,arr=arr)
    # User is not loggedin redirect to login page
    else:
        return redirect(url_for('doclogin'))

@app.route('/cancel_app/<string:id>', methods=['POST'])
def cancel_app(id):
    #create cursor
    if 'isdoctor' in session:
        cur = mysql.get_db().cursor()
        cur.execute("DELETE FROM booking WHERE Record_ID = %s", [id])
        mysql.get_db().commit()
        cur.close()
        #flash('Appointment is canceled', 'success')
        return redirect(url_for('curappointment'))
    else:
        return redirect(url_for('doclogin'))

@app.route('/approve_app/<string:id>', methods=['POST'])
def approve_app(id):
    if 'isdoctor' in session:
        #create cursor
        cur = mysql.get_db().cursor()
        cur.execute("UPDATE booking SET Status=1 WHERE Record_ID = %s", [id])
        mysql.get_db().commit()
        cur.close()
        #flash('Appointment is canceled', 'success')
        return redirect(url_for('curappointment'))
    else:
        return redirect(url_for('doclogin'))

@app.route('/cancelp_app/<string:id>', methods=['POST'])
def cancelp_app(id):
    if 'ispatient' in session:
        #create cursor
        cur = mysql.get_db().cursor()
        cur.execute("DELETE FROM booking WHERE Record_ID = %s", [id])
        mysql.get_db().commit()
        cur.close()
        #flash('Appointment is canceled', 'success')
        return redirect(url_for('appointments'))
    return redirect(url_for('login'))


class MessageForm(Form):    # Create Message Form
    body = StringField('', [validators.length(min=1)], render_kw={'autofocus': True})

@app.route('/chatting/<string:id>', methods=['GET', 'POST'])
def chatting(id):
    if 'ispatient' in session:
        
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.get_db().cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM doctors WHERE ID=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data[4]
            uid = session['id']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                # Create cursor
                cur = mysql.get_db().cursor()
                cur.execute("INSERT INTO messages(body, msg_by, msg_to) VALUES(%s, %s, %s)",
                            (txt_body, session['full_name'], session['name']))
                # Commit cursor
                mysql.get_db().commit()

            # Get users
            cur.execute("SELECT * FROM doctors")
            users = cur.fetchall()

            # Close Connection
            cur.close()
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            return render_template('chat_room.html', users=users, form=form, account=account)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/chattingh/<string:id>', methods=['GET', 'POST'])
def chattingh(id):
    if 'ispatient' in session:
        
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.get_db().cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM users WHERE ID=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data[5]
            uid = session['id']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                # Create cursor
                cur = mysql.get_db().cursor()
                cur.execute("INSERT INTO messages(body, msg_by, msg_to) VALUES(%s, %s, %s)",
                            (txt_body, uid, id))
                # Commit cursor
                mysql.get_db().commit()

            # Get users
            cur.execute("SELECT * FROM doctors")
            users = cur.fetchall()

            # Close Connection
            cur.close()
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            return render_template('chat_roomhome.html', users=users, form=form, account=account)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/chats', methods=['GET', 'POST'])
def chats():
    if 'isdoctor' in session:
        id = session['name']
        uid = session['full_name']
        # Create cursor
        cur = mysql.get_db().cursor()
        # Get message here
        cur.execute("SELECT * FROM messages WHERE (msg_by=%s AND msg_to=%s) OR (msg_by=%s AND msg_to=%s) "
                    "ORDER BY id ASC", (uid, id, id, uid))
        chats = cur.fetchall()
        # Close Connection
        cur.close()
        return render_template('chats.html', chats=chats,)
    return redirect(url_for('doclogin'))

@app.route('/docchatting/<string:id>', methods=['GET', 'POST'])
def docchatting(id):
    if 'isdoctor' in session:
        
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.get_db().cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM users WHERE ID=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data[5]
            uid = session['id']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                # Create cursor
                cur = mysql.get_db().cursor()
                cur.execute("INSERT INTO messages(body, msg_by, msg_to) VALUES(%s, %s, %s)",
                            (txt_body, session['full_name'], session['name']))
                # Commit cursor
                mysql.get_db().commit()
            
            curl = mysql.get_db().cursor()

            curl.execute("SELECT * FROM messages Where msg_to=%s", [session['full_name']])
            message = curl.fetchall()
            patient = set()
            for m in message:
                patient.add(m[2])
            # Get users
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            # Close Connection
            cur.close()
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            return render_template('docchat_room.html', users=users, form=form, account=account, patient=patient)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('doclogin'))


@app.route('/docchattingh/<string:id>', methods=['GET', 'POST'])
def docchattingh(id):
    if 'isdoctor' in session:
        
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.get_db().cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM doctors WHERE ID=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data[4]
            uid = session['id']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                # Create cursor
                cur = mysql.get_db().cursor()
                cur.execute("INSERT INTO messages(body, msg_by, msg_to) VALUES(%s, %s, %s)",
                            (txt_body, uid, id))
                # Commit cursor
                mysql.get_db().commit()
            curl = mysql.get_db().cursor()
            curl.execute("SELECT * FROM messages Where msg_to=%s", [session['name']])
            message = curl.fetchall()
            person = set()
            for m in message:
                person.add(m[2])
            # Get users
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            # Close Connection
            cur.close()
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            return render_template('docchat_roomhome.html', users=users, form=form, account=account, person=person)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('doclogin'))
@app.route('/docsensor/<string:id>', methods=['GET', 'POST'])
def docsensor(id):
    if 'isdoctor' in session:
        
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.get_db().cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM users WHERE ID=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data[5]
            uid = session['id']
            session['lid'] = id
            channel=l_data[11]
            temp=l_data[12]
            hum=l_data[13]
            puls=l_data[14]

            curl = mysql.get_db().cursor()

            curl.execute("SELECT * FROM messages Where msg_to=%s", [session['full_name']])
            message = curl.fetchall()
            patient = set()
            for m in message:
                patient.add(m[2])


            # Close Connection
            curl.close()

            # Get users
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            # Close Connection
            cur.close()
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            return render_template('docsensor.html', users=users, form=form, account=account, channel=channel, temp=temp, hum=hum, puls=puls, patient=patient)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('doclogin'))


@app.route('/docsensorh/<string:id>', methods=['GET', 'POST'])
def docsensorh(id):
    if 'isdoctor' in session:
        
        # Create cursor
        cur = mysql.get_db().cursor()
        curl = mysql.get_db().cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM doctors WHERE ID=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data[4]
            uid = session['id']
            session['lid'] = id

            # Get users
            curl.execute("SELECT * FROM messages Where msg_to=%s", [session['name']])
            message = curl.fetchall()
            person = set()
            for m in message:
                person.add(m[2])


            # Close Connection
            curl.close()
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            # Close Connection
            
            cur.close()
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            return render_template('docsensorhome.html', users=users,message=message ,account=account,person=person)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('doclogin'))


#Recommendation
@app.route('/recommending/<string:id>', methods=['GET', 'POST'])
def recommending(id):
    if 'ispatient' in session:
        
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.get_db().cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM doctors WHERE ID=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data[4]
            uid = session['id']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                # Create cursor
                cur = mysql.get_db().cursor()
                cur.execute("INSERT INTO recommendations(body, recommend_by, recommend_to) VALUES(%s, %s, %s)",
                            (txt_body, session['full_name'], session['name']))
                # Commit cursor
                mysql.get_db().commit()

            # Get users
            cur.execute("SELECT * FROM doctors")
            users = cur.fetchall()

            # Close Connection
            cur.close()
            curo = mysql.get_db().cursor()
            curo.execute("SELECT * FROM recommendations where recommend_by=%s", [session['name']])
            recom = curo.fetchall()
            curo.close()
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            return render_template('recommendation__room.html',recom=recom, users=users, form=form, account=account)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/recommendingh/<string:id>', methods=['GET', 'POST'])
def recommendingh(id):
    if 'ispatient' in session:
        
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.get_db().cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM users WHERE ID=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data[5]
            uid = session['id']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                # Create cursor
                cur = mysql.get_db().cursor()
                cur.execute("INSERT INTO recommendations(body, recommend_by, recommend_to) VALUES(%s, %s, %s)",
                            (txt_body, uid, id))
                # Commit cursor
                mysql.get_db().commit()

            # Get users
            cur.execute("SELECT * FROM doctors")
            users = cur.fetchall()

            # Close Connection
            cur.close()
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            return render_template('recommendation_roomhome.html', users=users, form=form, account=account)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/recommends', methods=['GET', 'POST'])
def recommends():
    if 'isdoctor' in session:
        id = session['name']
        uid = session['full_name']
        # Create cursor
        cur = mysql.get_db().cursor()
        # Get message here
        cur.execute("SELECT * FROM recommendations WHERE (recommend_by=%s AND recommend_to=%s) OR (recommend_by=%s AND recommend_to=%s) "
                    "ORDER BY id ASC", (uid, id, id, uid))
        chats = cur.fetchall()
        # Close Connection
        cur.close()
        return render_template('recommends.html', chats=chats,)
    return redirect(url_for('doclogin'))


@app.route('/docrecommending/<string:id>', methods=['GET', 'POST'])
def docrecommending(id):
    if 'isdoctor' in session:
        
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.get_db().cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM users WHERE ID=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data[5]
            uid = session['id']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                # Create cursor
                cur = mysql.get_db().cursor()
                cur.execute("INSERT INTO recommendations(body, recommend_by, recommend_to) VALUES(%s, %s, %s)",
                            (txt_body, session['full_name'], session['name']))
                # Commit cursor
                mysql.get_db().commit()

            curl = mysql.get_db().cursor()

            curl.execute("SELECT * FROM messages Where msg_to=%s", [session['full_name']])
            message = curl.fetchall()
            patient = set()
            for m in message:
                patient.add(m[2])


            # Close Connection
            curl.close()
            # Get users
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            # Close Connection
            cur.close()
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            return render_template('docrecommendation_room.html', users=users, form=form, account=account, patient=patient)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('doclogin'))


@app.route('/docrecommendingh/<string:id>', methods=['GET', 'POST'])
def docrecommendingh(id):
    if 'isdoctor' in session:
        
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.get_db().cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM doctors WHERE ID=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data[4]
            uid = session['id']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                # Create cursor
                cur = mysql.get_db().cursor()
                cur.execute("INSERT INTO recommendations(body, recommend_by, recommend_to) VALUES(%s, %s, %s)",
                            (txt_body, uid, id))
                # Commit cursor
                mysql.get_db().commit()
            
            curl = mysql.get_db().cursor()
            curl.execute("SELECT * FROM messages Where msg_to=%s", [session['name']])
            message = curl.fetchall()
            person = set()
            for m in message:
                person.add(m[2])

            # Get users
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            # Close Connection
            cur.close()
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM doctors WHERE ID = %s', [session['id']])
            account = cursor.fetchone()
            return render_template('docrecommendation_roomhome.html', users=users, form=form, account=account, person=person)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('doclogin'))

#ADMin functions 
@app.route('/viewuser')
def view():
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM users')
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()

        return render_template('view.html', data = data,account=account)
    else:
        return redirect(url_for('adminlogin'))    
@app.route('/viewdoctor')
def viewdoctor():
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM doctors')
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        return render_template('viewdoc.html', data = data,account=account)
    else:
        return redirect(url_for('adminlogin'))

#admin comment section
@app.route('/comment')
def comment():
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM contactus')
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()

        return render_template('comment.html', data = data,account=account)
    else:
        return redirect(url_for('adminlogin'))

@app.route('/add/')
def add():
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM users')
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        return render_template('add.html', data = data,account=account)
    else:
        return redirect(url_for('adminlogin'))

@app.route('/adduser', methods = ['POST', 'GET'])
def adduser():
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM users')
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        msg = ''
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            full_name = request.form['full_name']
            address = request.form['address']
            date = request.form['date']
            blood = request.form['blood']
            # Check if account exists using MySQL
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM users WHERE Username = %s', (username))
            account = cursor.fetchone()
            # If account exists show error and validation checks
            if account:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                # Account doesnt exists and the form data is valid, now insert new account into users table
                apistr = username;
                result = hashlib.md5(apistr.encode()) 
                comb = username+'(~)'+password
                s = comb.encode()
                s1 = pybase64.b64encode(s)
                api=s1.decode('utf-8')
                #print(s1)
                #r=pybase64.b64decode(s)
                #print(r.decode('utf-8'))
                curs = mysql.get_db().cursor()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                curs.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, NULL, %s, %s, %s, %s, %s,%s, NULL, NULL, NULL, NULL)', (username, hashed_password, email, full_name, address, blood, date, api,0))
                msg = 'User successfully registered!'
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
        # Show registration form with message (if any)
        
        flash(msg)
        return redirect(url_for('view', data = data,account=account))
    else:
        return redirect(url_for('adminlogin'))

@app.route('/update/<int:ID>/')
def update(ID):
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM users WHERE ID=%s", [ID])
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()

        if len(data) == 0:
            return redirect(url_for('view', data = data,account=account))
        else:
            session['update'] = ID
            return render_template('update.html', data = data,account=account)
    else:
        return redirect(url_for('adminlogin'))

#update HW admin
@app.route('/updatehw/<int:ID>/')
def updatehw(ID):
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM users WHERE ID=%s", [ID])
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()

        if len(data) == 0:
            return redirect(url_for('view', data = data,account=account))
        else:
            session['update'] = ID
            return render_template('updatehw.html', data = data,account=account)
    else:
        return redirect(url_for('adminlogin'))

@app.route('/updateuser', methods = ['POST'])
def updateuser():
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM users')
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        if request.method == 'POST' and request.form['update']:
            cursor.execute("UPDATE users set Username = %s, Email = %s, Full_Name= %s, Address= %s, Blood_Group=%s, Age = %s where ID = %s",
                            (request.form['Username'], request.form['Email'],request.form['Full_Name'],request.form['Address'],request.form['Blood_Group'],request.form['Age'],session['update']))

            flash('A user has been updated')

            session.pop('update', None)

            return redirect(url_for('view', data = data,account=account))
        else:
            return redirect(url_for('view', data = data,account=account))
    else:
        return redirect(url_for('adminlogin'))

# Update Admin hw
@app.route('/updateuserhw', methods = ['POST'])
def updateuserhw():
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM users')
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        if request.method == 'POST' and request.form['update']:
            cursor.execute("UPDATE users set Username = %s, channel = %s, temp = %s, humi= %s, pulse= %s where ID = %s",
                            (request.form['Username'], request.form['channel'], request.form['tempp'],request.form['hum'],request.form['puls'],session['update']))

            flash('A user has been updated')

            session.pop('update', None)

            return redirect(url_for('view', data = data,account=account))
        else:
            return redirect(url_for('view', data = data,account=account))
    else:
        return redirect(url_for('adminlogin'))

@app.route('/delete/<int:ID>/')
def delete(ID):
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM users WHERE ID=%s", [ID])
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()

        if len(data) == 0:
            return redirect(url_for('view', data = data,account=account))
        else:
            session['delete'] = ID
            return render_template('delete.html', data = data,account=account)
    else:
        return redirect(url_for('adminlogin'))

@app.route('/deleteuser', methods = ['POST'])
def deleteuser():
    if 'isadmin' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        if request.method == 'POST' and request.form['delete']:

            cur = mysql.get_db().cursor()
            cur.execute("SELECT * FROM users")
            data = cur.fetchall()
            cursor.execute("DELETE FROM users where ID = %s", (session['delete']))
            flash('A user has been deleted')

            session.pop('delete', None)

            return redirect(url_for('view'))
        else:
            return redirect(url_for('view'))

    else:
        return redirect(url_for('adminlogin'))
@app.route('/addoc/')
def addoc():
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM doctors')
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        return render_template('adddoc.html', data = data,account=account)
    else:
        return redirect(url_for('adminlogin'))
@app.route('/adddoc', methods = ['POST', 'GET'])
def adddoc():
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM doctors')
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        msg = ''
        # Check if "username", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            full_name = request.form['full_name']
            registration_number = request.form['registration_number']
            contact_number = request.form['contact_number']
            spec = request.form['specialization']
            address = request.form['address']

            # Check if account exists using MySQL
            cursor = mysql.get_db().cursor()
            cursor.execute('SELECT * FROM doctors WHERE Username = %s', (username))
            accou = cursor.fetchone()
            # If account exists show error and validation checks
            if accou:
                msg = 'Account already exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                # Account doesnt exists and the form data is valid, now insert new account into users table
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                print(username + "\n" + str(hashed_password)+ "\n" + email+ "\n" +full_name+ "\n" +registration_number+ "\n" +contact_number+ "\n" +spec+ "\n" +address)
                cursor.execute('INSERT INTO doctors VALUES (NULL, %s, %s, %s, %s, %s, %s ,%s, %s, %s, %s)', ( username, hashed_password, email, full_name, registration_number, contact_number, "" , spec, address ,0))
                msg = 'Doctor successfully registered!'
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            msg = 'Please fill out the form!'
        # Show registration form with message (if any)
        flash(msg)
        return redirect(url_for('viewdoctor', data = data,account=account))
    else:
        return redirect(url_for('adminlogin'))
@app.route('/updatedc/<int:ID>/')
def updatedc(ID):
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM doctors WHERE ID=%s", [ID])
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()

        if len(data) == 0:
            return redirect(url_for('viewdoctor', data = data,account=account))
        else:
            session['update'] = ID
            return render_template('updatedoc.html', data = data,account=account)
    else:
        return redirect(url_for('adminlogin'))
@app.route('/updatedoc', methods = ['POST'])
def updatedoc():
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM doctors')
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        if request.method == 'POST' and request.form['update']:
            #cursor.execute("UPDATE doctors set Username = %s, Email = %s, Full_Name= %s, Registration_Number= %s, Contact_Number=%s,  Specialization = %s, Address = %s where ID = %s",
            #                  (request.form['Username'], request.form['Email'],request.form['Full_Name'],request.form['registration_number'],request.form['contact_number'],request.form['specialization'],request.form['address'],session['update']))
            cursor.execute("UPDATE doctors set Username = %s, Email = %s, Full_Name= %s, Address = %s, Registration_Number= %s, Contact_Number=%s,  Specialization = %s where ID = %s",
                            (request.form['Username'], request.form['Email'], request.form['Full_Name'],request.form['Address'], request.form['registration_number'],request.form['contact_number'],request.form['specialization'], session['update']))
            flash('A doctor has been updated')

            session.pop('update', None)

            return redirect(url_for('viewdoctor', data = data,account=account))
        else:
            return redirect(url_for('viewdoctor', data = data,account=account))
    else:
        return redirect(url_for('adminlogin'))
#update doctor account
@app.route('/updatedocacc', methods = ['POST'])
def updatedocacc():
    if 'isdoctor' in session:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM doctors')
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        if request.method == 'POST' and request.form['update']:
            #cursor.execute("UPDATE doctors set Username = %s, Email = %s, Full_Name= %s, Registration_Number= %s, Contact_Number=%s,  Specialization = %s, Address = %s where ID = %s",
            #                  (request.form['Username'], request.form['Email'],request.form['Full_Name'],request.form['registration_number'],request.form['contact_number'],request.form['specialization'],request.form['address'],session['update']))
            cursor.execute("UPDATE doctors set Username = %s, Email = %s, Full_Name= %s, Address = %s, Registration_Number= %s, Contact_Number=%s,  Specialization = %s where ID = %s",
                            (request.form['Username'], request.form['Email'], request.form['Full_Name'],request.form['Address'], request.form['registration_number'],request.form['contact_number'],request.form['specialization'], session['update']))
            flash('A doctor has been updated')

            session.pop('update', None)

            return redirect(url_for('docaccount'))
        else:
            return redirect(url_for('docaccount'))
    else:
        return redirect(url_for('doclogin'))

@app.route('/deletedo/<int:ID>/')
def deletedc(ID):
    if 'isadmin' in session:
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM doctors WHERE ID=%s", [ID])
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()

        if len(data) == 0:
            return redirect(url_for('viewdoctor', data = data,account=account))
        else:
            session['delete'] = ID
            return render_template('deletedoc.html', data = data,account=account)
    else:
        return redirect(url_for('adminlogin'))
@app.route('/deletedoc', methods = ['POST'])
def deletedoc():
    if 'isadmin' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        if request.method == 'POST' and request.form['delete']:

            cur = mysql.get_db().cursor()
            cur.execute("SELECT * FROM doctors")
            data = cur.fetchall()
            cursor.execute("DELETE FROM doctors where ID = %s", (session['delete']))
            flash('A doctor has been deleted')

            session.pop('delete', None)

            return redirect(url_for('viewdoctor'))
        else:
            return redirect(url_for('viewdoctor'))
    else:
        return redirect(url_for('adminlogin'))

#delete comment
@app.route('/deletecom/<int:ID>/')
def deletecom(ID):
    if 'isadmin' in session:
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        cursor.execute("DELETE FROM contactus where ID = %s", [ID])
        flash('A comment has been deleted')


        return redirect(url_for('comment'))
    else:
        return redirect(url_for('adminlogin'))
#Audio video Consultancy
@app.route('/consultancy')
def consultancy():
    if 'loggedin' in session:
        
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM users WHERE ID = %s', [session['id']])
        account = cursor.fetchone()
        
        return render_template('audiovideo.html', account=account)
    return redirect(url_for('/'))

@app.route("/meeting/<uid>")
def meeting(uid):
     return render_template("meeting.html")
    


@socketio.on('newUser')
def newUser(msg):
    print('New user: '+msg)
    data = json.loads(msg)
    print(data["username"])
    newuser = user.User(data["username"], data["meetingID"], data["userID"])
    users.append(newuser)
    emit('newUser',msg, broadcast=True)


@socketio.on('checkUser')
def checkUser(msg):
    data = json.loads(msg)
    existing = False
    for user in users:
        print(user.username)
        if(data["username"] == user.username):
            if(data["meetingID"] == user.meetingID):
                existing = True
    if (existing):
        send('userExists', broadcast=False)
    else:
        send('userOK', broadcast=False)


@socketio.on('userDisconnected')
def onDisconnect(msg):
    i = 0
    posArray = 0
    data = json.loads(msg)
    for user in users:
        if(data["username"] == user.username):
            if(data["meetingID"] == user.meetingID):
                posArray = i
        i = i + 1
    users.pop(posArray)
    print("user "+ data["username"]+ " from meeting "+data["meetingID"]+ " disconnected")
    emit('userDisconnected',msg, broadcast=True)
    
@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

#Update personal profile
@app.route('/updatemy/<int:ID>/')
def updatemy(ID):
    if 'ispatient' in session:
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM users WHERE ID=%s", [ID])
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()

        if len(data) == 0:
            return redirect(url_for('view', data = data,account=account))
        else:
            session['update'] = ID
            return render_template('updatemy.html', data = data,account=account)
    else:
        return redirect(url_for('login'))
#Update doctor profile
@app.route('/updatedocpro/<int:ID>/')
def updatedocpro(ID):
    if 'isdoctor' in session:
        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM doctors WHERE ID=%s", [ID])
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        session['update'] = ID
        return render_template('updatedocpro.html', data = data,account=account)
    else:
        return redirect(url_for('doclogin'))
@app.route('/updateusermy', methods = ['POST'])
def updateusermy():
    if 'ispatient' in session:
        cur = mysql.get_db().cursor()
        cur.execute('SELECT * FROM users')
        data = cur.fetchall()
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM admin WHERE Username = %s', [session['username']])
        account = cursor.fetchone()
        if request.method == 'POST' and request.form['update']:
            cursor.execute("UPDATE users set Username = %s, Email = %s, Full_Name= %s, Address= %s, Blood_Group=%s, Age = %s where ID = %s",
                            (request.form['Username'], request.form['Email'],request.form['Full_Name'],request.form['Address'],request.form['Blood_Group'],request.form['date'],session['update']))

            flash('A user has been updated')

            session.pop('update', None)

            return redirect(url_for('myaccount', data = data,account=account))
        else:
            return redirect(url_for('myaccount', data = data,account=account))
    else:
        return redirect(url_for('login'))
# forgot User password
@app.route('/userpasforgot', methods = ['POST','GET'])
def userpasforgot():
        if request.method == "POST":
            email = request.form["email"]
            token = str(uuid.uuid4())
            cur = mysql.get_db().cursor()
            result = cur.execute("SELECT * FROM users Where email=%s",[email])
            if result>0:
                data = cur.fetchone()
                msg = Message(subject="Forgot password request ", sender="chalielijalem@gmail.com", recipients=[email])
                msg.body = render_template("sent.html", token=token, data=data)
                mail.send(msg)
                cur = mysql.get_db().cursor()
                cur.execute("UPDATE users SET token=%s Where email=%s",[token,email])
                mysql.get_db().commit()
                cur.close()
                flash("Email already sent to your email", "success")
                return redirect('/userpasforgot')
            else:
                flash("Email do not match","danger")

        return render_template('userforgot.html')

# reset User password
@app.route('/userpassreset/<token>', methods = ['POST','GET'])
def userpassreset(token):
    if 'loggedin' in session:
        return redirect('/')
    if request.method == "POST":
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        token1 = str(uuid.uuid4())
        if password != confirm_password:
            flash("Password donot match", "danger")
            return redirect("userpassreset")
        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur = mysql.get_db().cursor()
        m=cur.execute("SELECT * FROM users Where token=%s",[token])
        user = cur.fetchone()
        if m>0:
            cur = mysql.get_db().cursor()
            cur.execute("UPDATE users SET token=%s, password=%s WHERE token=%s",[token1, password, token])
            mysql.get_db().commit()
            cur.close()
            flash("Your password successfully updated","success")
            return redirect("/login")
        else:
            flash("Your Token is invalid", "danger")
            return redirect('/')
    return render_template('userreset.html')

 # Contact Us storing messages to database
@app.route("/contact",methods=["Post"])
def contact():
    # Getting data from inout fields and storing them in these variables
    if request.method == "POST":
        name= request.form["name"]
        email=request.form['email']
        phone=request.form['phone']
        message=request.form['message']
        cur = mysql.get_db().cursor()
        cur.execute('INSERT INTO ContactUs VALUES (NULL,%s, %s, %s,%s)', ( name, email, phone, message))
        mysql.get_db().commit()
        cur.close()
        flash("Your message successfully sent","success")
        return redirect("/#contact")
    return render_template('index.html')     
      
@app.route('/adminlogout')
def adminlogout():
   # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.clear()
   # Redirect to login page
   return redirect(url_for('index'))

# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
   # Remove session data, this will log the user out
   cur = mysql.get_db().cursor()
   x = '0'
   uid=session['id']
   if(session['isdoctor']==0):
       cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
   else:
       cur.execute("UPDATE doctors SET online=%s WHERE id=%s", (x, uid))
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.clear()
   # Redirect to login page
   return redirect(url_for('index'))

#run the Flask Server
if __name__ == '__main__':
    socketio.run(app)
#"""-------------------------------End of Web Application-------------------------------"""