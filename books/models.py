from auth.models import db
from datetime import datetime


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10,2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'),nullable=False)
    faculty = db.relationship('Faculty',backref=db.backref('posts', lazy=True))

    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'),nullable=False)
    subject = db.relationship('Subject',backref=db.backref('posts', lazy=True))

    image = db.Column(db.String(150),nullable=False,default='image.jpg')

    def __repr__(self):
        return '<Post %r>' % self.title


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