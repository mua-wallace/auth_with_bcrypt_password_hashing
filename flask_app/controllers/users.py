from flask_app import app
from flask_bcrypt import Bcrypt  
from flask import render_template, redirect,request,session,flash
from flask_app.models.user import User

bcrypt = Bcrypt(app)


@app.route('/')
def auth():
    return render_template('auth.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/process', methods=["POST"])
def process():
    # validate the form here ...
     # if there are errors:
    # We call the staticmethod on User model to validate
    if not User.validate_user(request.form):
        # redirect to the route where the user form is rendered.
        return redirect('/')
    # create the hash
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "name":request.form['name'],
        "email": request.form['email'],
        "dob": request.form['dob'],
        "password": hashed_pw
        
    }
    id = User.save(data)
    print('3'*70)
    print(id)
    session['user_id'] = id
    return redirect('/home')


@app.route('/process-login', methods =['POST'])
def login_user():
    data = {
        'email':request.form['email']
    }
    
    user = User.get_user_by_email(data)
    if not user:
        flash("Invalid credentials", 'login')
        return redirect('/login')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid credentials", 'login')
        return redirect('/login')
    
    session['user_id'] = user.id
    return redirect('/home')


@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['user_id']
    }
    return render_template('home.html', user = User.get_user_by_id(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')