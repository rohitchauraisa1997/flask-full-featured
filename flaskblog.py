from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "rohit97"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60),nullable=False)
    # Meaning
    # posts Attribute adds a relationship to the post model
    # referring to Post Model Class
    # backref is similar to having another col in the Posts Model to get the 
    # author attribute to get the user who created the post.
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # remember not to use paranthesis in datetime.utcnow as it will return the
    # default to be time at that period of time rather than passing the datetime.utcnow
    # function.
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # relationship to User model 
    # user is table here hence the smallcasing of user in user.id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

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
        flash(f'Account Created for {form.username.data}!!', 'success')
        return redirect(url_for('home'))
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

if __name__ == '__main__':
    app.run(debug=True)