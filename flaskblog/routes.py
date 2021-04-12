from flask import  render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import db, bcrypt

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

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "rohit@google.com" and form.password.data == 'password':
            flash(f'You have logged in!!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check username and password','danger')
    return render_template('login.html',title='Login', form=form)
