import os
import secrets

from flask import url_for
from flask_mail import Message
from flaskblog import app, mail
from PIL import Image


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

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',\
        sender='noreply@demo.com',\
        recipients=[user.email])
    # _external = True enables us to get absolute url.
    msg.body = f''''
    To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)} 

If you did not make this request simply ignore the email.
'''
    mail.send(msg)

