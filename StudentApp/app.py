from flask import Flask, request,render_template, flash, redirect, url_for, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators,SelectField,IntegerField, ValidationError
from wtforms.validators import Email
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ' '
app.config['MYSQL_DB'] = 'StudentApp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home.html')

def validate_rollno(form,field):   
    txt = field.data
    if('@' in txt):
        x = list(map(int, txt.split("@")))
        if(x[0]<1 or x[0]>12):
            raise ValidationError("Invalid Rollno!")
        if(x[1]<1 or x[1]>35):
            raise ValidationError("Invalid Rollno!")
    else:
        raise ValidationError("Invalid Rollno(Roll no must be of the form class@rollno eg: 3@20)")

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=3, max=50)])
    rollno = StringField('Roll no', [validators.Length(min=3), validate_rollno])
    email = StringField('E-mail', [validators.Email()])
    standard = SelectField(u"Choose standard", coerce=int,choices=[("1","1"),("2","2"),("3","3"),("4","4"),("5","5"),("6","6"),("7","7"),("8","8"),("9","9"),("10","10"),("11","11"),("12","12")],validate_choice=False)
    password = PasswordField('Password',[validators.Length(min=8, max=100), validators.EqualTo("confirm", "Passwords do not match")])
    confirm = PasswordField('Repeat Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if(request.method == 'POST' and form.validate()):
        name = form.name.data
        rollno = form.rollno.data
        Email = form.email.data
        standard = form.standard.data
        password = sha256_crypt.encrypt(str(form.password.data))
        # Create cursor
        cur = mysql.connection.cursor()

        #check whether the email is already registered

        result = cur.execute("select EMAIL from StudentApp where EMAIL = %s",[Email])
        # Execute query
        if(result>0):
            cur.close()
            flash("AN ACCOUNT EXISTS WITH THIS EMAIL!","danger")
            return redirect(url_for("login"))
        else:
            cur.execute("INSERT INTO StudentApp(ROLL_NO, NAME,EMAIL,PASSWORD,STANDARD) VALUES(%s, %s, %s, %s,%s)",(rollno, name, Email, password, standard))

            # Commit to DB
            mysql.connection.commit()

            session['registered']= True
            session['standard']= standard
            session['rollno']= rollno

            # Close connection
            cur.close()

        if(standard >1) :
            flash('Enter the details', 'success')

            return redirect(url_for('grades'))
        else :
            flash('Registration successful', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

def is_registered_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if('registered' in session):
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please Register', 'danger')
            return redirect(url_for('register'))
    return wrap

#Grades
@app.route('/grades', methods=['GET', 'POST'])
@is_registered_in
def grades():
    if(request.method == 'POST'):
        
        standard= request.form.getlist('standard')
        grade = request.form.getlist('grade')
        remark = request.form.getlist("remark")
        percentage = request.form.getlist("percentage")

        rollno = session['rollno']

        cur = mysql.connection.cursor()

        for i in range(0,session['standard']-1):
            cur.execute('INSERT INTO Grades(ROLLNO,STANDARD,GRADE,REMARK,PERCENTAGE) VALUES (%s,%s,%s,%s,%s)', (rollno,standard[i],grade[i],remark[i],percentage[i]))
            mysql.connection.commit()
        
        cur.close()
        session.clear()

        flash("Registation successful! You can now Log in!", "success")

        return redirect(url_for("login"))
    return render_template('grades.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM StudentApp WHERE EMAIL = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['PASSWORD']
            print(password)
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                #flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))

            else:
                flash("Invalid Login!","danger")
                render_template('login.html')
            cur.close()
        else:
            flash("Username not found!","danger")
            render_template('login.html')
    return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if('logged_in' in session):
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("You have now logged out", 'success')
    return redirect(url_for('login'))


#Dashboard
@app.route('/dashboard', methods=['GET','POST'])
@is_logged_in
def dashboard():
    email = session['username']
    cur = mysql.connection.cursor()

    #Get the rollno of the user
    result = cur.execute("select ROLL_NO from StudentApp where EMAIL = %s",[email])
    data = cur.fetchone()
    rollno = data['ROLL_NO']

    #fetch the grades

    res = cur.execute("select * from Grades where ROLLNO = %s",[rollno])
    data = cur.fetchall()
    cur.close()
    if(res > 0):
        return render_template('dashboard.html', grades=data)
    else:
        msg = "There are no Education Details Available"
        flash(msg,"danger")
        return render_template('dashboard.html', msg=msg)
if __name__=='__main__':
    app.secret_key="123@#%^&"
    app.run(debug=True)