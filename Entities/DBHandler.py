from db import db
from Entities.Teacher import Teacher
from Entities.Classroom import Classroom
from Entities.Student_Classroom import Student_Classroom
from Entities.Student import Student
from Entities.Skill import Skill
from Entities.TestPaper import TestPaper
from Entities.Skill_TestPaper import Skill_TestPaper
from Entities.Test_Result import Test_Result
from Entities.Classroom_TestPaper import Classroom_TestPaper


class DBHandler:

    #If true then database exceptions will print to screen
    DEBUG_MODE = True

    def get_classroom_by_teacher(t_id):
        query = Classroom.query.filter_by(t_id=t_id)
        return query


