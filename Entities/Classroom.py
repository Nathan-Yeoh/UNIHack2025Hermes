from db import db

class Classroom(db.model):
    __tablename__ = "Classroom"

    cl_id = db.Column(db.Integer, primary_key=True)
    t_id = db.Column(db.Integer, db.ForeignKey("Teacher.t_id", ondelete="CASCADE"), nullable=False)