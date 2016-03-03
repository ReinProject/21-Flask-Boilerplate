from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import and_
from flask.ext.login import UserMixin

class Extra(db.Model):
    ''' Extra data for job display. '''
    __tablename__ = 'extra'
    __bind_key__ = 'spectacle'
    job_id = db.Column(db.String, primary_key=True)
    visible = db.Column(db.Boolean)

    def __init__(self, job_id):
        self.job_id = job_id
        self.visible = 0

    @classmethod
    def hide(self, job_id):
        e = db.session.query(self).filter(self.job_id == job_id).first()
        if e:
            e.visible = 0
        else:
            e = Extra(job_id)
            db.session.add(e)
        db.session.commit()

    @classmethod
    def isvisible(self, job_id):
        extra = db.session.query(Extra).filter(Extra.job_id == job_id).first()
        if extra and extra.visible == 0:
            return False
        return True

class User(db.Model, UserMixin):
    ''' A website user. '''
    __tablename__ = 'users'
    __bind_key__ = 'spectacle'
    name = db.Column(db.String)
    surname = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String, primary_key=True)
    confirmation = db.Column(db.Boolean)
    _password = db.Column(db.String)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)

    def get_id(self):
        return self.email

