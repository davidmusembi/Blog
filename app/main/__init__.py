from flask import Blueprint

main = Blueprint('main', __name__)
# try:
from app.main import views
# except:
#     print('*'*50,"Error","*"*50)
