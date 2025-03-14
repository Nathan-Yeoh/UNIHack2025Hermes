from db import db

class Test_Result(db.model):
    __tablename__ = "Test_Result"

    cl_id = db.Column(db.Integer, db.ForeignKey("Classroom.cl_id", ondelete="CASCADE"), primary_key=True)
    tp_id = db.Column(db.Integer, db.ForeignKey("TestPaper.tp_id", ondelete="CASCADE"), primary_key=True)
    tp_question_no = db.Column(db.Integer, db.ForeignKey("TestPaper.tp_question_no", ondelete="CASCADE"), primary_key=True)
    s_id = db.Column(db.Integer, db.ForeignKey("Student.s_id", ondelete="CASCADE"), primary_key=True)