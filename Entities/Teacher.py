from db import db

class Teacher(db.Model):
    __tablename__ = "Teacher"

    t_id = db.Column(db.Integer, primary_key=True)
    t_username = db.Column(db.String(20), nullable=False)

    