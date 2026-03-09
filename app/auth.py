
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from urllib.parse import urlparse 
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from app.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        error = None

        if(not username):
            error = 'Username is required.'
        elif(not password):
            error = 'Password is required.'
        else:
            user = db.session.query(User).filter(User.username == username).scalar()
            if(user):
                error = 'User {} is already registered.'.format(username)

            if(error is None):
                user = User(username=username, password_hash=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                flash('Congratulations, you are now a registered user!')
                return redirect(url_for('auth.login'))
            else:
                flash(error)

    return render_template('auth/register.html', page_title="Registrieren")


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db.session.query(User).filter(User.username == username).scalar()

        if(user is None):
            error = 'Incorrect username.'
        elif(not user.check_password(password)):
            error = 'Incorrect password.'

        if(error is None):
            login_user(user)
            return redirect(url_for('kalender.index'))

        flash(error)
    return render_template('auth/login.html', page_title="Anmelden")


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
