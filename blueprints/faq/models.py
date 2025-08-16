from extensions import db


class Faq(db.Model):
    __tablename__ = 'faq'

    fid = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)