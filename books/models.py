
from auth.models import db
from datetime import datetime


class Book(db.Model):
    __searchbale__ = ['name','desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    con = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'),nullable=False)
    faculty = db.relationship('Faculty',backref=db.backref('posts', lazy=True))

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'),nullable=False)
    subject = db.relationship('Subject',backref=db.backref('posts', lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('books', lazy=True))

    image = db.Column(db.String(150),nullable=False,default='image.jpg')
    is_original = db.Column(db.Boolean, default=True, nullable=False)

    ratings = db.relationship('Rating', backref='book_ratings', lazy=True)

    def __repr__(self):
        return self.name
    
class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    name = db.Column(db.String(80), db.ForeignKey('book.name'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    con = db.Column(db.Text, nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

    faculty = db.relationship('Faculty', backref=db.backref('stock_entries', lazy=True))
    subject = db.relationship('Subject', backref=db.backref('stock_entries', lazy=True))
    user = db.relationship('User', backref=db.backref('stock_entries', lazy=True))

    def __repr__(self):
        return f"<Stock {self.id}>"



class Faculty(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False,unique=True)

    def __repr__(self):
        return self.name

class Subject(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False,unique=True)

    def __repr__(self):
        return self.name
