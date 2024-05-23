# imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
# ------------------------------- CODE ---------------------------------------------

db = SQLAlchemy()

# Create User table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    student_id = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    bio = db.Column(db.String(200),default=None)
    profile_pic = db.Column(db.String(200),default="default_pfp.png")


    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, student_id={self.student_id})"