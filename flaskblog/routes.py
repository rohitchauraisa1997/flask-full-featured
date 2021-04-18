from operator import pos
import secrets
import os
from PIL import Image
from flask import  render_template, url_for, flash, redirect, request, abort
from flaskblog import app
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog import db, bcrypt
from flask_login import login_user, logout_user, current_user, login_required

# posts = [
#     {
#         'title':'One Piece',
#         'author': 'Eichiro Oda',
#         'content': 'one piece chapter 1',
#         'date_posted': 'Oct 1, 1997'
#     },
#     {
#         'title':'Naruto',
#         'author': 'Masashi Kishimoto',
#         'content': 'Naruto chapter 1',
#         'date_posted': 'Oct 1, 1997'
#     }
# ]

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
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
            # helps redirecting us to correct route
            # Exmaple:- in case we directly went for route...
            # http://127.0.0.1:5000/account
            # it will take us to login page first and then when we 
            # login correctly it takes us to account.
            # print("&"*100)
            # print(request.args)
            # print("&"*100)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    # saves the image to our filesystem
    # randomising the name of image with random hex.
    random_hex = secrets.token_hex(8)
    file_name, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # resizing the picture before saving
    # as only 125px gets rendered and also
    # memory gets wasted. 
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # saves image to filesystem
    i.save(picture_path)
    return picture_fn

@app.route("/account",methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        
    image_file = url_for("static", filename="profile_pics/{}".format(current_user.image_file))
    return render_template('account.html',title='Account', image_file=image_file, form=form) 

@app.route("/post/new",methods=['GET', 'POST'])
@login_required
def new_post():
    form =PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your Post has been created.")
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend="Add Post")

@app.route("/post/<int:post_id>")
def post(post_id):
    # give post with this id else return get_or_404
    # that is post doesnt exist.
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update",methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    # give post with this id else return get_or_404
    # that is post doesnt exist.
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        # forbidden route 403
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        print("="*30)
        print(form.title.data)
        print(form.content.data)
        print("="*30)
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post has been updated", category='success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title="Update Post", form=form, legend="Update Post")

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))