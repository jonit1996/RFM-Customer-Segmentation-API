from model.db import db

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(255))
    recency = db.Column(db.Float)
    frequency = db.Column(db.Integer)
    monetary = db.Column(db.Float)
    rfm_score = db.Column(db.Float)
    customer_group = db.Column(db.String(255))
    clv = db.Column(db.Float)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "recency": self.recency,
            "frequency": self.frequency,
            "monetary": self.monetary,
            "rfm_score": self.rfm_score,
            "customer_group": self.customer_group,
            "clv": self.clv
        }
