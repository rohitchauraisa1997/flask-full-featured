from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
# __name__ is a special variable in python
# that is the name of the module this tells 
# flask where to look for the tmplates, static files etc.
# print(__name__)

app = Flask(__name__)

# secret key protects against modifying cookies,
# crossite requests and forgery attacks.
app.config['SECRET_KEY'] = "rohit97"

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

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html',title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)