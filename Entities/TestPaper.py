from db import db, Column

class TestPaper(db.model):
    __tablename__ = "TestPaper"

    tp_id = Column(db.Integer, primary_key=True)
    tp_question_no = Column(db.Integer, primary_key=True)
    tp_question_text = Column(db.String(200), nullable=False)
