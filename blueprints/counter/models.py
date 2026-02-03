from extensions import db


class Counter(db.Model):
    __tablename__ = "keymetrics"

    id = db.Column(db.Integer, primary_key=True)
    icon = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
