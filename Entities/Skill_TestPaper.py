from db import db, Column

class Skill_TestPaper(db.model):
    __tablename__ = "Skill_TestPaper"

    tp_id = Column(db.Integer, db.ForeignKey("TestPaper.tp_id", ondelete="CASCADE"), primary_key=True)
    tp_question_no = Column(db.Integer, db.ForeignKey("TestPaper.tp_question_no", ondelete="CASCADE"), primary_key=True)
    sk_id= Column(db.Integer, db.ForeignKey("Skill.sk_id", ondelete="CASCADE"), primary_key=True)