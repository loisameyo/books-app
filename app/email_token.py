import os
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

from app import create_app, mail
config_name = os.getenv('FLASK_CONFIG')

app = create_app(config_name)

def generate_reset_password_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

def confirm_reset_password_token():
    pass