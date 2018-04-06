from flask import Flask
# from models import User

app = Flask (__name__)
app.url_map.strict_slashes = False
app.secret_key = 'secret'


from app import views