from auth.models import db
from datetime import datetime

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(80), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    date_order = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('invoices', lazy=True))
     

    def __repr__(self):
        return f"<Invoice {self.invoice}>"