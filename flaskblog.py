from flask import Flask
# __name__ is a special variable in python
# that is the name of the module this tells 
# flask where to look for the tmplates, static files etc.
# print(__name__)

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def hello_world():
    return '<h3>Hello, World!</h3>'

@app.route('/about')
def about():
    return '<h3>Hello, About Page</h3>'

if __name__ == '__main__':
    app.run(debug=True)