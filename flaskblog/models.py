from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
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

    def get_reset_token(self,expires_sec=1800):
        '''
        >>> from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
        >>> s = Serializer('secret', 30)
        >>> token = s.dumps({'user_id':1}.decode('utf-8'))
        >>> token
            'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYyMDQ4ODY2MCwiZXhwIjoxNjIwNDg4NjkwfQ.eyJ1c2VyX2lkIjoxfQ.JVWZ_lpCxs1wNW9wZi3s5_qLMMDYkD6c8PQYdxpxoArT2hnjy5a6fMbcxdtTipwvJdmZmQce9qlA398DtzPqyw'
        >>> s.loads(token)
            {'user_id': 1}
        '''
        s = Serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
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
