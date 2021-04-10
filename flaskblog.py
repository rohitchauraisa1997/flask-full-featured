from flask import Flask, render_template, url_for
# __name__ is a special variable in python
# that is the name of the module this tells 
# flask where to look for the tmplates, static files etc.
# print(__name__)

app = Flask(__name__)

# secret key protects against modifying cookies,
# crossite requests and forgery attacks.
app.config['secret_key'] = "rohit97"

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
def hello_world():
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html',title="About")

if __name__ == '__main__':
    app.run(debug=True)