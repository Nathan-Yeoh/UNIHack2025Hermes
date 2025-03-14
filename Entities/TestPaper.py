from db import db

class TestPaper(db.model):
    __tablename__ = "TestPaper"

    tp_id = db.Column(db.Integer, primary_key=True)
    tp_question_no = db.Column(db.Integer, primary_key=True)
    tp_question_text = db.Column(db.String(200), nullable=False)
