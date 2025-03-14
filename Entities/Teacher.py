from db import db, Column

class Teacher(db.model):
    __tablename__ = "Teacher"

    t_id = Column(db.Integer, primary_key=True)
    t_username = Column(db.String(20), nullable=False)

    