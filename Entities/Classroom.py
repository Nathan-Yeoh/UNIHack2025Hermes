from Entities import Student, Teacher
from db import db

class Classroom(db.Model):
    __tablename__ = "Classroom"

    cl_id = db.Column(db.String(7), primary_key=True)
    t_id = db.Column(db.Integer, db.ForeignKey("Teacher.t_id", ondelete="CASCADE"), nullable=False)

    def addClassroomStudent(self, student: Student):
        """
        Adds a student to the classroom object
        :return:
        """
        pass

    def setClassroomTeacher(self, t_id: int) -> None:
        """
        Sets the teacher for a particular classroom

        :param t_id:
        :return:
        """
        self.t_id = t_id