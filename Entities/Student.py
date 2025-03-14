from db import db

class Student(db.Model):
    __tablename__ = "Student"

    s_id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(20), nullable=False)