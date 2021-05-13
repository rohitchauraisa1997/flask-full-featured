from flask import (Blueprint, abort, flash, redirect, render_template, request,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user
from flaskblog import bcrypt, db, mail
from flaskblog.models import Post, User
from flaskblog.users.forms import (LoginForm, RegistrationForm,
                                   RequestResetForm, ResetPasswordForm,
                                   UpdateAccountForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users',__name__)


@users.route("/register",methods=['GET','POST'])
def register():
    # if user is already logged in redirect to home.
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        print(user)
        db.session.add(user)
        db.session.commit()
        flash(f'Account Created for {form.username.data}!! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('register.html',title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # helps redirecting us to correct route
            # Exmaple:- in case we directly went for route...
            # http://127.0.0.1:5000/account
            # it will take us to login page first and then when we 
            # login correctly it takes us to account.
            # print("&"*100)
            # print(request.args)
            # print("&"*100)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account",methods=['GET', 'POST'])
@login_required
def account():
    print("*"*100)
    print(current_user.username)
    print(current_user.image_file)
    print(current_user.email)
    print("*"*100)
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # updating user's username, picture and email.
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your Account has been updated", category="success")
        # redirecting them to the account page.
        # doing redirect for post/get redirect pattern.
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for("static", filename="profile_pics/{}".format(current_user.image_file))
    return render_template('account.html',title='Account', image_file=image_file, form=form) 

@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page',default=1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # posts = Post.query.all()
    print("*"*50)
    print(user)
    print("*"*50)
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html',posts=posts, user=user)

@users.route("/reset_password",methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print("-"*50)
        print(user)
        print("-"*50)
        send_reset_email(user)
        flash('An Email has been sent with instructions to reset ur email', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title="Reset Password", form=form)

@users.route("/reset_password/<token>",methods=['GET', 'POST'])
def reset_token(token):
    print("%"*50)
    print(token)
    print("%"*50)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    print("^"*50)
    print(user)
    print("^"*50)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print(user)
        user.password = hashed_password
        db.session.commit()
        flash(f'Your Password has been updated', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title="Reset Password", form=form) 
