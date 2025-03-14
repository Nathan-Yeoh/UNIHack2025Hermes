from db import db, Column

class Classroom(db.model):
    __tablename__ = "Classroom"

    cl_id = Column(db.Integer, primary_key=True)
    t_id = Column(db.Integer, db.ForeignKey("Teacher.t_id", ondelete="CASCADE"), nullable=False)