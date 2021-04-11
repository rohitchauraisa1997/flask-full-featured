from datetime import datetime
from flaskblog import db

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
