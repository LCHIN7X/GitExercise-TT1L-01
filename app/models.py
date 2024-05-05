from flask_sqlalchemy import SQLAlchemy
from auth.models import db

db = SQLAlchemy()

from flask_sqlalchemy import SQLAlchemy

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Quantity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    quantity_id = db.Column(db.Integer, db.ForeignKey('quantity.id'), nullable=False)
    price_id = db.Column(db.Integer, db.ForeignKey('price.id'), nullable=False)
    photo = db.Column(db.String(255), nullable=False)
    remark = db.Column(db.Text)

    faculty = db.relationship('Faculty', backref=db.backref('books', lazy=True))
    subject = db.relationship('Subject', backref=db.backref('books', lazy=True))
    quantity = db.relationship('Quantity', backref=db.backref('books', lazy=True))
    price = db.relationship('Price', backref=db.backref('books', lazy=True))