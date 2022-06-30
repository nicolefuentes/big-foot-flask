from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password']),
        "confirm": request.form['confirm'],
        "bio": request.form['bio']
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user=User.get_by_id(data)
    sighting=Sighting.get_all()
    return render_template("dashboard.html",user=user, sighting=sighting)

@app.route('/edit-profile')
def edit_profile():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("edit-profile.html",user=User.get_by_id(data))

@app.route('/user/update',methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.validate_user_update(request.form):
        return redirect('/edit-profile')
    data ={
        'id': session['user_id'],
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'bio': request.form['bio']
    }
    User.update(data)
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')