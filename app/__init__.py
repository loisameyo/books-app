from flask import Flask
# from models import User

app = Flask (__name__)
app.url_map.strict_slashes = False


from app import views