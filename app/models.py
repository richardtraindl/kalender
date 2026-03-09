
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from app import login_manager, db


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User %r>' % (self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Termin(db.Model):
    __tablename__ = 'termin'

    id = db.Column(db.Integer, db.Sequence('termin_id_seq'), primary_key=True)
    autor = db.Column(db.String(30))
    beginn = db.Column(db.DateTime(timezone=False), nullable=False)
    ende = db.Column(db.DateTime(timezone=False), nullable=False)
    thema = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<termin %r>' % (self.id)
