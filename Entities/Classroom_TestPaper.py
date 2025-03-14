from db import db

class Classroom_TestPaper(db.Model):
    __tablename__ = "Classroom_TestPaper"

    cl_id = db.Column(db.String(7), db.ForeignKey("Classroom.cl_id", ondelete="CASCADE"), primary_key=True)
    tp_id = db.Column(db.Integer, db.ForeignKey("TestPaper.tp_id", ondelete="CASCADE"), primary_key=True)
    cltp_name = db.Column(db.String(30), nullable=False) #name of test paper - not on the diagram :/

    