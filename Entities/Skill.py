from db import db


class Skill(db.Model):
    __tablename__ = "Skill"

    # GENERAL ATTRIBUTES
    sk_id = db.Column(db.Integer, primary_key=True)
    sk_name = db.Column(db.String(20), nullable=False)
    sk_desc = db.Column(db.String(200), nullable=False)