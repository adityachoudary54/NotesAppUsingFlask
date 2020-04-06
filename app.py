from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'#//// for absolute path /// for relative
db=SQLAlchemy(app)

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    createdDate = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    modifiedDate = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User',backref=db.backref('notes', lazy=True))#imp
    def __repr__(self):
        return '<Notes %r>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(36), nullable=False)
    login=db.Column(db.Boolean,nullable=False,default=False)
    def __repr__(self):
        return '<User %r>' % self.name

@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method=='POST':
        userName=request.form['name']
        userPassword=request.form['password']
        newUser=User(name=userName,password=userPassword)
        try:
            db.session.add(newUser)
            db.session.commit()
            return redirect('/admin')
        except:
            return "Some error occured while adding user to the admin"
    else:
        users=User.query.order_by(User.id).all()
        return render_template('admin.html',users=users)

@app.route('/',methods=['GET','POST'])
def login():
    if request.method=='POST':
        userName=request.form['name']
        userPassword=request.form['password']
        user=User.query.filter_by(name=userName).first()
        if user is None or userPassword!=user.password:
            return redirect('/')
        else:
            user.login=True
            db.session.commit()
            print(user.login)
            return redirect('/notes/{}'.format(user.id))
    else:
        return render_template('login.html')

@app.route('/notes/<int:id>')
def userNotes(id):
    user=User.query.get_or_404(id)
    if user.login==False:
        return "Unauthorized Access"
    else:
        return render_template("notes.html",user=user)

@app.route('/notes/add/<int:id>',methods=['GET','POST'])
def userNotesAdd(id):
    user=User.query.get_or_404(id)
    if request.method=='POST':
        if user.login==False:
            return "Unauthorized Access"
        else:
            note=Notes(content=request.form['content'])
            user.notes.append(note)
            db.session.commit()
            return redirect('/notes/{}'.format(user.id))
    else:
        return render_template("notes.html",user=user)

@app.route('/notes/update/<int:userid>/<int:id>',methods=['GET','POST'])
def userNotesUpdate(userid,id):
    user=User.query.get_or_404(userid)
    note=Notes.query.get_or_404(id)
    if request.method=='POST':
        note.content=request.form['content']
        note.modifiedDate=datetime.utcnow()
        db.session.commit()
        return redirect('/notes/{}'.format(userid))
    else:
        return render_template("notes.html",user=user)


@app.route('/notes/delete/<int:userid>/<int:id>')
def userNotesDelete(userid,id):
    note=Notes.query.get_or_404(id)
    try:
        print(note)
        db.session.delete(note)
        db.session.commit()
        return redirect('/notes/{}'.format(userid))
    except:
        return "Error occured while deleting element"

@app.route('/notes/logout/<int:id>')
def userNotesLogout(id):
    user=User.query.get_or_404(id)
    try:
        user.login=False
        db.session.commit()
        return redirect("/")
    except:
        return "Some error occured while logging out"
    
if __name__=="__main__":
    app.run()