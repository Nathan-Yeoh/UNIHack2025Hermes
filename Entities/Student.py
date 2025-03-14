from db import db, Column

class Student(db.model):
    __tablename__ = "Student"

    s_id = Column(db.Integer, primary_key=True)
    s_name = Column(db.String(20), nullable=False)