
import os
from re import U
from flask import Flask,session,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']='fdojfdoj2'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key =True)
    nom = db.Column(db.String(64),index=True)
    notem= db.Column(db.Integer,index=True)
    notei= db.Column(db.Integer,index=True)
class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key =True)
    identifiant = db.Column(db.String(64), unique=True, index=True)
    password=db.Column(db.String(64),nullable=False)  

class RegistrationForm(FlaskForm):
    identifiant= StringField('identifiant', validators=[DataRequired(), Length(min=2,max=20)])
    password=PasswordField('Password', validators=[DataRequired()])
    submit=SubmitField('valider')

class NotesForm(FlaskForm):
    nom=StringField('nom', validators=[DataRequired(), Length(min=2,max=20)])
    notem= IntegerField('notem', validators=[DataRequired()])
    notei=IntegerField('notei', validators=[DataRequired()])
    submit=SubmitField('valider')

db.create_all()

@app.route('/',methods=['post','get'])
def login():
    myform=RegistrationForm()
    if myform.validate_on_submit():
        res=Admin.query.filter_by(identifiant=myform.identifiant.data,password=myform.password.data).first()
        if res == None:
            return redirect(url_for('login'))
        else:
            session['user']=res.identifiant
            return redirect(url_for('note'))
    return render_template('login.html',form=myform)
@app.route('/note',methods=['post','get'])
def note():
    myform=NotesForm()
    if myform.validate_on_submit():
        U=User(nom=myform.nom.data,notem=myform.notem.data,notei=myform.notei.data)
        db.session.add(U)
        db.session.commit()
        return redirect(url_for('edit'))
    return render_template('note.html',form=myform)    

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect(url_for('login'))

@app.route('/edit')
def edit():
    res=User.query.all()
    return render_template('edit.html',ress=res)   

@app.route('/del/<user>')
def dell(user):
    User.query.filter_by(nom=user).delete()
    db.session.commit()
    return redirect(url_for('edit'))

@app.route('/edit0/<user>')
def edit0(user):
    User.query.filter_by(nom=user).delete()
    db.session.commit()
    return redirect(url_for('note'))    

if __name__=='__main__':
    app.run(debug=True)    