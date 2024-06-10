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

class InvoiceItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    invoice = db.relationship('Invoice', backref=db.backref('items', lazy=True))
    book = db.relationship('Book')

    def __repr__(self):
        return f"<InvoiceItem {self.id}>"

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    book = db.relationship('Book', backref=db.backref('book_ratings', lazy=True))
    invoice = db.relationship('Invoice', backref=db.backref('ratings', lazy=True))  