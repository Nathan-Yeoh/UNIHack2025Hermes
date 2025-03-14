from db import db, Column

class Student_Classroom(db.model):
    __tablename__ = "Student_Classroom"

    cl_id = Column(db.Integer, db.ForeignKey("Classroom.cl_id", ondelete="CASCADE"), primary_key=True)
    s_id = Column(db.Integer, db.ForeignKey("Student.s_id", ondelete="CASCADE"), primary_key=True)
    