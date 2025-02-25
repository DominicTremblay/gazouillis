from flask import Flask, flash, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_seeder import FlaskSeeder

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

seeder = FlaskSeeder()
seeder.init_app(app, db)

login = LoginManager(app)
login.login_view = 'ouvrir_session'

# Personnaliser le message pour access non autorise
@login.unauthorized_handler
def unauthorized():
    flash("Veuillez vous connecter pour accéder à cette page.")
    return redirect(url_for('ouvrir_session'))


from app import routes, modeles,erreurs