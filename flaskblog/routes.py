from flask import  render_template, url_for, flash, redirect, request
from flaskblog import app
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required

posts = [
    {
        'title':'One Piece',
        'author': 'Eichiro Oda',
        'content': 'one piece chapter 1',
        'date_posted': 'Oct 1, 1997'
    },
    {
        'title':'Naruto',
        'author': 'Masashi Kishimoto',
        'content': 'Naruto chapter 1',
        'date_posted': 'Oct 1, 1997'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title="About")

@app.route("/register",methods=['GET','POST'])
def register():
    # if user is already logged in redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        print(user)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.username.data}!! You are now able to log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html',title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    print("*"*100)
    print(current_user.username)
    print(current_user.image_file)
    print(current_user.email)
    print("*"*100)
    return render_template('account.html',title='Account') 