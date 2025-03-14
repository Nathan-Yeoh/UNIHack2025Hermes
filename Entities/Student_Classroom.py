from db import db

class Student_Classroom(db.model):
    __tablename__ = "Student_Classroom"

    cl_id = db.Column(db.Integer, db.ForeignKey("Classroom.cl_id", ondelete="CASCADE"), primary_key=True)
    s_id = db.Column(db.Integer, db.ForeignKey("Student.s_id", ondelete="CASCADE"), primary_key=True)
    