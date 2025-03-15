from db import db

class TestPaper(db.Model):
    __tablename__ = "TestPaper"

    tp_id = db.Column(db.Integer, primary_key=True)
    tp_question_no = db.Column(db.Integer, primary_key=True)
    tp_question_text = db.Column(db.String(200), nullable=False)
    tp_question_total_mark = db.Column(db.Integer, nullable=False)
    