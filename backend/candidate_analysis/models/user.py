from candidate_analysis.framework.db import db
from candidate_analysis.sql_methods.user.dummy_users import dummy_insert_users_query
import hashlib

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(256))

    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def insert_dummy_users(cls):
        return db.engine.execute(dummy_insert_users_query())

    def is_authorized(self, password):
        return self.password == hashlib.sha3_256(password.encode()).hexdigest()
