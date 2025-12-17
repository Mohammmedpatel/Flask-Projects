from sqlalchemy import func
from app import db

class Notes(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    data= db.Column(db.Text, nullable=False)
    date= db.Column(db.DateTime, default=func.now())
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"))