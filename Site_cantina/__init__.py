from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os

UPLOADFOLDER = os.path.join('Site_cantina/static', 'produtos')
ALLOWEDEXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/cantina"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "94500175985c5d5b14e01f17718c9285"
app.config['UPLOAD_FOLDER'] = UPLOADFOLDER

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
login.login_view = "login"
login.login_message_category = 'info'


from Site_cantina import routes  # Importar rotas após inicialização do app

# Importar modelos após inicialização do banco de dados
from Site_cantina.models import User  # Exemplo de importação de modelo
