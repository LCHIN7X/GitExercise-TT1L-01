# from flask_sqlalchemy import SQLAlchemy
from auth.models import db

# db = SQLAlchemy() 

class SecondHandBooks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), nullable=False)
    subject = db.Column(db.String(20), nullable=False)
    quanity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.String(10), nullable=False)
    photo = db.Column(db.Text(), nullable=False)
    remark = db.Column(db.Text(), nullable=False)
    faculty = db.Column(db.String(20), nullable=False)

    __tablename__ = "second_hand_books"


    def __repr__(self):
        return f"SecondHandBooks(id={self.id}, student_id={self.student_id}, subject={self.subject}, quantity={self.quantity}, price={self.price}, photo={self.photo}, remark={self.remark}, faculty={self.faculty})"
    
class shbooks_Faculty(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        name = db.Column(db.String(30),nullable=False,unique=True)



class shbooks_Subject(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(30),nullable=False,unique=True)