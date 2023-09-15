from flask_app import app
from flask import render_template, redirect


@app.route('/')
def auth():
    return render_template('auth.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/process', methods=["POST"])
def process():
    
    return redirect('/home')


@app.route('/home')
def home():
    return render_template('home.html')