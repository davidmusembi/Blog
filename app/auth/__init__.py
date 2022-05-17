from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='templates/auth')
from app.auth import views, forms
