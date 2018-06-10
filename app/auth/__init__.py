from flask import Blueprint

auth = Blueprint('auth', __name__)

from app.views import views