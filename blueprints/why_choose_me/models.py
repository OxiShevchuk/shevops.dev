from extensions import db


class Reason(db.Model):
    __tablename__ = 'reasons'

    id = db.Column(db.Integer, primary_key=True)
    sort_order = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)