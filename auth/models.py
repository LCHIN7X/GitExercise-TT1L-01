# imports
from flask_sqlalchemy import SQLAlchemy
# ------------------------------- CODE ---------------------------------------------

db = SQLAlchemy()

# Create User table
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    student_id = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)