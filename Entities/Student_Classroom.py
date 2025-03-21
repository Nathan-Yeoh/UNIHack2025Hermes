from db import db


class Student_Classroom(db.Model):
    __tablename__ = "Student_Classroom"

    cl_id = db.Column(db.String(7), db.ForeignKey("Classroom.cl_id", ondelete="CASCADE"), primary_key=True)
    s_id = db.Column(db.Integer, db.ForeignKey("Student.s_id", ondelete="CASCADE"), primary_key=True)

    student = db.relationship("Student", backref="classrooms")

    def get_cl_id(self):
        return self.cl_id

    def get_s_id(self):
        return self.s_id
