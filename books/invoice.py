from auth.models import db
from datetime import datetime

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(80),unique=True, nullable=False)
    status = db.Column(db.String(20),default='Pending', nullable=False)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    user = db.relationship('User', backref=db.backref('books', lazy=True))
    data_order = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return '<Invoice %r>' % self.invoice