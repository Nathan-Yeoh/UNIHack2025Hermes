from db import db

class TestPaper(db.Model):
    __tablename__ = "TestPaper"

    tp_id = db.Column(db.Integer, primary_key=True)
    tp_question_no = db.Column(db.Integer, primary_key=True)
    tp_question_text = db.Column(db.String(200), nullable=False)
    tp_question_total_mark = db.Column(db.Integer, nullable=False)

    def get_question_id(self):
        return self.tp_id

    def get_question_no(self):
        return self.tp_question_no

    def get_question_text(self):
        return self.tp_question_text

    def get_question_total_mark(self):
        return self.tp_question_total_mark