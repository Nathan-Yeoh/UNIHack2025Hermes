from db import db

class Test_Result(db.Model):
    __tablename__ = "Test_Result"

    cl_id = db.Column(db.String(7), db.ForeignKey("Classroom.cl_id", ondelete="CASCADE"), primary_key=True)
    tp_id = db.Column(db.Integer, db.ForeignKey("TestPaper.tp_id", ondelete="CASCADE"), primary_key=True)
    tp_question_no = db.Column(db.Integer, db.ForeignKey("TestPaper.tp_question_no", ondelete="CASCADE"), primary_key=True)
    s_id = db.Column(db.Integer, db.ForeignKey("Student.s_id", ondelete="CASCADE"), primary_key=True)
    tr_mark = db.Column(db.Integer, nullable = False)

    def get_cl_id(self):
        return self.cl_id

    def get_tp_id(self):
        return self.tp_id

    def get_tp_question_no(self):
        return self.tp_question_no

    def get_s_id(self):
        return self.s_id

    def get_student_mark(self):
        return self.tr_mark

    def set_student_mark(self, mark: float = 0):
        self.tr_mark = mark