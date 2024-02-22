from flask import Flask, render_template, request,redirect, make_response, session,flash
from flask_session import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "abc"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
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


@app.route('/')
def getFirstPage():
    return render_template("firstpage.html")

# Login Route which leads to main page if the login is successfull
@app.route('/login', methods=['GET','POST'])
def getToLogin():
    if request.method=='POST':
        uname= request.form['uname']
        passw= request.form['passw']
        session["name"] = uname
        s=session["name"]
        emp = Employees.query.all()
        if uname =='Harini' and passw=='98':
            return render_template('main.html', names=s, data=emp)
        else:
            flash("Invalid Username or Password")
            return render_template('login.html')
    if request.method =='GET':
        return render_template('login.html')

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
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    age = request.form.get("age")
    salary = request.form.get("salary")
    location = request.form.get("location")

    if first_name != '' and last_name != '' and age is not None:
        p = Employees(first_name=first_name, last_name=last_name, age=age, salary=salary,location=location)
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
    app.run(port=1997)