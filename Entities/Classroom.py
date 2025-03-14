from db import db

class Classroom(db.Model):
    __tablename__ = "Classroom"

    cl_id = db.Column(db.String(7), primary_key=True)
    t_id = db.Column(db.Integer, db.ForeignKey("Teacher.t_id", ondelete="CASCADE"), nullable=False)