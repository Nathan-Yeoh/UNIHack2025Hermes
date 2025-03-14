from db import db

class Skill_TestPaper(db.Model):
    __tablename__ = "Skill_TestPaper"

    tp_id = db.Column(db.Integer, db.ForeignKey("TestPaper.tp_id", ondelete="CASCADE"), primary_key=True)
    tp_question_no = db.Column(db.Integer, db.ForeignKey("TestPaper.tp_question_no", ondelete="CASCADE"), primary_key=True)
    sk_id= db.Column(db.Integer, db.ForeignKey("Skill.sk_id", ondelete="CASCADE"), primary_key=True)