
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta


app = Flask(__name__)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kalender.sqlite3'
app.config['SECRET_KEY'] = 'esgibtnichtmehrvielzusagen'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=1440) # 24h

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import auth
app.register_blueprint(auth.bp)

from . import kalender
app.register_blueprint(kalender.bp)
    
from .util.filters import calc_kw, add_days, add_hours, add_mins, gib_feiertag
app.jinja_env.filters['calc_kw'] = calc_kw
app.jinja_env.filters['add_days'] = add_days
app.jinja_env.filters['add_hours'] = add_hours
app.jinja_env.filters['add_mins'] = add_mins
app.jinja_env.filters['feiertag'] = gib_feiertag
