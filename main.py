from flask import Flask, render_template, request,redirect,jsonify, make_response, session,flash
from flask_session import *
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from sqlalchemy import create_engine
# from sqlalchemy import Table, Column, Integer, String, MetaData
# meta = MetaData()
#
# students = Table(
#    'students', meta,
#    Column('id', Integer, primary_key = True),
#    Column('name', String),
#    Column('lastname', String),
# )
# engine = create_engine('sqlite:///emp.db', echo = True)
# meta.create_all(engine)

app = Flask(__name__)
app.secret_key = "abc"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


db = SQLAlchemy(app)
ma = Marshmallow(app)
@app.before_request
def create_tables():
    db.create_all()

class Employees(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"first_name=first_name, last_name=last_name, age=age, salary=salary,location=location"

class Empp(ma.SQLAlchemySchema):
    class Meta:
        fields = ("first_name","last_name","age","salary","location")

employee_obj = Empp()
employee_objs = Empp(many=True)


class sample(db.Model):
    __tablename__ = 'sample'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"first_name=first_name, last_name=last_name, age=age, salary=salary,location=location"


class User(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(20), unique=False, nullable=False)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"email_id=email_id,first_name=first_name, last_name=last_name,password=password"

class users(ma.SQLAlchemySchema):
    class Metas:
        fields = ("email_id","first_name","last_name","password")

user_obj = users()
user_objs = users(many=True)

# Below code was written to branch out the creation of emp using JSON
# @app.route('/empObj',methods = ['POST'])
# def add_emp():
#     first_name = request.json["first_name"]
#     last_name = request.json["last_name"]
#     age = request.json['age']
#     salary = request.json['salary']
#     location = request.json['location']
#
#     my_emp = Employees(first_name=first_name, last_name=last_name, age=age, salary=salary,location=location)
#     db.session.add(my_emp)
#     db.session.commit()
#     return employee_obj.jsonify(my_emp)

@app.route('/')
def getFirstPage():
    return render_template("firstpage.html")

# Login Route which leads to main page if the login is successfull
@app.route('/login', methods=['GET','POST'])
def getToLogin():
    if request.method=='POST':
        uname= request.form['uname']
        passw= request.form['passw']
        emp = Employees.query.all()
        register = User.query.all()
        for reg in register:
            if uname == reg.email_id and passw== reg.password:
                session["name"] = reg.first_name+' '+ reg.last_name
                s = session["name"]
                return render_template('main.html', names=s, data=emp)
        else:
                flash("Invalid Username or Password")
                return render_template('login.html')
    if request.method =='GET':
        return render_template('login.html')

@app.route('/register')
def getToRegister():
    return render_template('register.html')

@app.route('/registered',methods=['POST'])
def getToLoginAgain():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email_id = request.form.get("email_id")
    password = request.form.get("password")
    if first_name != '' and last_name != '':
        u = User(email_id=email_id, first_name=first_name, last_name=last_name, password=password)
        db.session.add(u)
        db.session.commit()
        return render_template('login.html')

# Route to Main Page, using session to store the username after login
@app.route('/mainPage')
def getToMainPage():
    emp = Employees.query.all()
    s = session["name"]
    return render_template('main.html', names=s,data=emp)

@app.route('/create', methods=['GET','POST'])
def getToCreate():
        return render_template('createemp.html')

@app.route('/created',methods=['POST'])
def getToCreated():
    if request.headers['Content-Type'] == 'application/json':
            api_first_name = request.json["first_name"]
            api_last_name = request.json["last_name"]
            api_age = request.json['age']
            api_salary = request.json['salary']
            api_location = request.json['location']
            api_create = Employees(first_name=api_first_name, last_name=api_last_name, age=api_age, salary=api_salary, location=api_location)
            db.session.add(api_create)
            db.session.commit()
            return employee_obj.jsonify(api_create)
    else:
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        age = request.form.get("age")
        salary = request.form.get("salary")
        location = request.form.get("location")
        if first_name != '' and last_name != '' and age is not None:
                p = Employees(first_name=first_name, last_name=last_name, age=age, salary=salary, location=location)
                db.session.add(p)
                db.session.commit()
                return redirect('/mainPage')
        else:
                return redirect('/mainPage')

@app.route('/updateForm/<int:id>')
def getToUpdate(id):
    result = db.session.execute(db.select(Employees).filter_by(id=id)).scalar_one()
    return render_template('updateform.html',res=result)

@app.route('/updated/<int:id>',methods=['POST'])
def getToUpdated(id):
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    age = request.form.get("age")
    salary = request.form.get("salary")
    location = request.form.get("location")

    if first_name != '' and last_name != '' and age is not None:
        p1 = Employees.query.filter_by(id=id).update(dict(first_name=first_name, last_name=last_name, age=age, salary=salary,location=location))
        db.session.commit()
        return redirect('/mainPage')
    else:
        return redirect('/mainPage')

@app.route('/delete/<int:id>')
def getToDel(id):
    flash("Record Deleted")
    Employees.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect('/mainPage')

@app.route('/logout')
def getToLogout():
    session.pop('name',None)
    return render_template("logout.html")

if __name__ == '__main__':
    app.run(port=1999)