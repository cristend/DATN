from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    license_id = db.Column(db.Integer, unique=True)
    # _license = db.relationship('License', backref='user')
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    group = db.Column(db.Integer, default=0, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        server_onupdate=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Labels(db.Model):
    __tablename__ = 'labels'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(256))

    def __repr__(self):
        return '<Labels {}>'.format(self.label)


class License(db.Model):
    __tablename__ = 'licenses'
    id = db.Column(db.Integer, primary_key=True)
    # license_id = db.Column(db.Integer, db.ForeignKey(
    #     'users.license_id'), nullable=False)
    license_id = db.Column(db.Integer, nullable=False)
    assigned = db.Column(db.Boolean, default=False, nullable=False)
    revoked = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<License {}>'.format(self.id)


class Media(db.Model):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    detail = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<Media {}>'.format(self.name)
