from db import db


class Student(db.Model):
    __tablename__ = "Student"

    s_id = db.Column(db.Integer, primary_key=True)
    s_name = db.Column(db.String(20), nullable=False)

    def get_s_id(self):
        return self.s_id

    def get_s_name(self):
        return self.s_name
