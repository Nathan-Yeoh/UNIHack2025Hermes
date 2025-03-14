from db import db, Column


class Skill(db.model):
    __tablename__ = "Skill"

    sk_id = Column(db.Integer, primary_key=True)
    sk_name = Column(db.String(20), nullable=False)
    sk_desc = Column(db.String(200), nullable=False)