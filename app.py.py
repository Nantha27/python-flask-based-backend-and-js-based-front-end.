from enum import unique
from flask import Flask,render_template,url_for,redirect,request,flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import RadioField,SelectMultipleField
from cProfile import label

app=Flask(__name__)

app.config['SECRET_KEY'] = "ngkcoders27011998"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datamodel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50),unique=True)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    gender = RadioField(label='Gender',choices=['Male','female'])
    subject = SelectMultipleField(u'Subject of User', choices=[
        ('mech', 'Mechanical'),
        ('it','information')
        ('cse', 'Computer'),
        ('ece','Electronic')
        ('eee', 'Electrical')
    ])

    def __init__(self, name, email, phone, subject):
        self.name = name
        self.email = email
        self.phone = phone
        self.subject = subject

@app.route('/')
def Index():
    all_data = User.query.all()
    return render_template("index.html", guest_data =all_data )

@app.route('/insert', methods = ['post'])
def insert():
     if request.method == 'POST':
 
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
 
 
        user_data = User(name, email, phone, subject)
        db.session.add(user_data)
        db.session.commit()
 
        flash("User_data Inserted Successfully")
 
        return redirect(url_for('Index'))

@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        user_data = User.query.get(request.form.get('id'))
 
        user_data.name = request.form['name']
        user_data.email = request.form['email']
        user_data.phone = request.form['phone']
        user_data.subject = request.form['subject']
 
        db.session.commit()
        flash("User_data Updated Successfully")
 
        return redirect(url_for('Index'))
 
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    user_data = User.query.get(id)
    db.session.delete(user_data)
    db.session.commit()
    flash("User_data Deleted Successfully")
 
    return redirect(url_for('Index'))



if __name__ == "__main__":
    app.run(debug=True)