from auth.models import db
from datetime import datetime

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(80),unique=True, nullable=False)
    status = db.Column(db.String(20),default='Pending', nullable=False)
    data_order = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.name