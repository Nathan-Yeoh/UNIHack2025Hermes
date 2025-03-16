from Entities.Student import Student
from Entities.Classroom import Classroom
from Entities.Student_Classroom import Student_Classroom
from Entities.TestPaper import TestPaper
from Entities.Teacher import Teacher
from Entities.Skill import Skill
from Entities.Skill_TestPaper import Skill_TestPaper
from Entities.Test_Result import Test_Result
from Entities.Classroom_TestPaper import Classroom_TestPaper
from Entities.PDF_upload import PDF_upload
from db import db

def _print(s):
    """
    Print the string if we are in debug mode
    """
    if DBHandler.DEBUG_MODE:
        print(s)

class DBHandler:
    """
    This class inherits the SQLAlchemy database
    Methods are added to allow updating CRUD operations for each respective type (User, Task, ProductBacklog, Sprint)
    """
    # If true then database exceptions will print to screen
    DEBUG_MODE = True

    # === CLASSROOM METHODS === #

    @staticmethod
    def get_all_classrooms() -> list[Classroom]:
        """
        Returns a list of all classrooms within the database

        :param:
        :return:
        """
        try:
            return Classroom.query.all()
        except Exception as e:
            _print(e)
            return -1

    @staticmethod
    def get_num_classrooms() -> int:
        """
        Returns the total number of classrooms currently stored within the app

        :param:
        :return:
        """
        pass

    @staticmethod
    def add_classroom(classroom: Classroom) -> int:
        """
        Adds a classroom, and sets the teacher
        :param classroom:
        :return:
        """
        try:
            db.session.add(classroom)
            db.session.commit()
            return 0

        except:
            # In case of database error
            db.session.rollback()
            return 1

    @staticmethod
    def get_testpapers_by_classroom(cl_id: str) -> list[TestPaper]:
        """
        Returns a list of tuples formatted as (test paper ID, test paper name, TestPaper objects) given the classroom ID as a string
        :param cl_id:
        :return:
        """
        try:
            return Classroom_TestPaper.query.filter_by(cl_id=cl_id).all()

        except Exception as e:
            _print(e)
            return -1

    @staticmethod
    def get_students_by_classroom(cl_id: str) -> list[tuple[int, str]]:
        """
        Returns the list of student IDs as a list of integers

        :param cl_id:
        :return:
        """
        try:
            students = []
            records = Student_Classroom.query.join(Student, Student_Classroom.s_id == Student.s_id).filter(Student_Classroom.cl_id ==
                                                                                                          cl_id).all()
            for record in records:
                students.append((record.student.s_id, record.student.s_name))

            return students
        except Exception as e:
            _print(e)
            return -1

    # === STUDENT METHODS === #

    @staticmethod
    def get_student_by_id(s_id: int) -> Student:
        """
        Returns the student object from their ID number

        :param s_id:
        :return:
        """
        try:
            return Student.query.get(s_id)
        except Exception as e:
            _print(e)
            return -1


    @staticmethod
    def get_classroom_by_teacher(t_id):
        query = Classroom.query.filter_by(t_id=t_id)
        return query

    # === SKILL METHODS === #
    @staticmethod
    def get_all_skill_names():
        return [x[0] for x in db.session.query(Skill.sk_name).all()]
    
    # === TEST_RESULT METHODS === #
    
    @staticmethod
    def get_attribute_values(s_id, cl_id):
        studrecords = db.session.query(Test_Result, TestPaper, Skill_TestPaper).filter(
                        Test_Result.s_id==s_id).join(
                        TestPaper, (TestPaper.tp_id == Test_Result.tp_id) & (TestPaper.tp_question_no == Test_Result.tp_question_no)).join(
                        Skill_TestPaper, (TestPaper.tp_question_no == Skill_TestPaper.tp_question_no) & (TestPaper.tp_id == Skill_TestPaper.tp_id)).with_entities(
                        Test_Result.s_id, TestPaper.tp_id, TestPaper.tp_question_no, Skill_TestPaper.sk_id, TestPaper.tp_question_total_mark, Test_Result.tr_mark)
        
        records = db.session.query(Classroom_TestPaper, Test_Result, TestPaper, Skill_TestPaper ).filter(
                        Classroom_TestPaper.cl_id == cl_id).join(
                        Test_Result,Classroom_TestPaper.tp_id == Test_Result.tp_id).join(
                        TestPaper, (TestPaper.tp_id == Test_Result.tp_id) & (TestPaper.tp_question_no == Test_Result.tp_question_no)).join(
                        Skill_TestPaper, (TestPaper.tp_question_no == Skill_TestPaper.tp_question_no) & (TestPaper.tp_id == Skill_TestPaper.tp_id)).with_entities(
                        Test_Result.s_id, TestPaper.tp_id, TestPaper.tp_question_no, Skill_TestPaper.sk_id, TestPaper.tp_question_total_mark, Test_Result.tr_mark, Classroom_TestPaper)

        skills = Skill.query.all()
        studattributes = []
        attributes = []

        for skill in skills:
            studquery = studrecords.filter(Skill_TestPaper.sk_id==skill.sk_id).all()
            query = records.filter(Skill_TestPaper.sk_id==skill.sk_id).all()


            studtotalMark = [x[5] * 100 for x in studquery]
            totalMark = [x[5] * 100 for x in query]
            # print(studtotalMark)

            try:
                studattributes.append(sum(studtotalMark)/len(studtotalMark))
            except:
                studattributes.append(0)
            
            try:
                attributes.append(sum(totalMark)/len(totalMark))
            except:
                attributes.append(0)
    
        return studattributes, attributes
    
    @staticmethod
    def get_attribute_per_question(tp_id):
        # skills for all questions
        query_skills = db.session.query(TestPaper, Skill_TestPaper, Skill).filter(
                        (TestPaper.tp_id == tp_id)).join(
                        Skill_TestPaper, (TestPaper.tp_question_no == Skill_TestPaper.tp_question_no) & (TestPaper.tp_id == Skill_TestPaper.tp_id)).join(
                        Skill, (Skill_TestPaper.sk_id == Skill.sk_id)).with_entities(
                        TestPaper.tp_id, TestPaper.tp_question_no, Skill_TestPaper.sk_id, Skill.sk_name)
        
        # question query
        query_questions = db.session.query(TestPaper).filter(TestPaper.tp_id == tp_id).with_entities(TestPaper.tp_question_no)
        records_questions = query_questions.all()

        question_attributes = []
        for question_no in records_questions:
            records_skills = query_skills.filter(TestPaper.tp_question_no == question_no).all()
            attributes = ""

            for skills in records_skills:
                attributes += skills[-1]

            try:
                question_attributes.append(attributes)
            except:
                pass
    
        return question_attributes


    @staticmethod
    def get_test_result(cl_id:str, tp_id: int, tp_question_no: int, s_id: int) -> Test_Result:
        try:
            return Test_Result.query.get((cl_id, tp_id, tp_question_no, s_id))
        except Exception as e:
            _print(e)
            return -1

    # === TEST PAPER METHODS === #
    @staticmethod
    def get_testpaper_by_cltp_id(cl_id: str, tp_id: int) -> TestPaper:
        """
        Returns a Classroom_TestPaper object from input of classroom ID and test paper ID

        :param cl_id:
        :param tp_id:
        :return:
        """
        try:
            return Classroom_TestPaper.query.get((cl_id, tp_id))
        except Exception as e:
            _print(e)
            return -1


    @staticmethod
    def get_testquestions_by_tp_id(tp_id: int) -> list[tuple[str, int]]:
        """
        Takes the classroom ID and test paper ID and outputs a list of tuples organised as (question string, marks available)

        :param tp_id:
        :return:
        """
        try:
            return TestPaper.query.filter_by(tp_id=tp_id).all()

        except Exception as e:
            _print(e)
            return -1

    @staticmethod
    def update_testquestion_by_tp_question_id(tp_id: int, tp_question_no: int, tp_question_text: str, tp_question_total_mark: int):
        """
        Takes an input of the test paper ID and question number ID, and updates the values

        :param tp_question_total_mark:
        :param tp_question_text:
        :param tp_id:
        :param tp_question_no:
        :return:
        """
        try:
            question = TestPaper.query.get((tp_id, tp_question_no))
            question.set_question_text(tp_question_text)
            question.set_question_total_mark(tp_question_total_mark)

            db.session.commit()
            return 0

        except Exception as e:
            _print(e)
            return -1
    
    @staticmethod
    def add_to_classroom_testpaper(cl_id: str, tp_id: int, cltp_name: str):
        insert = Classroom_TestPaper(cl_id=cl_id, tp_id=tp_id, cltp_name=cltp_name)
        db.session.add(insert)
        db.session.commit()
        return 0
    
    @staticmethod
    def add_to_testpaper(tp_id, tp_question_no, tp_question_text, tp_question_total_mark):
        insert = TestPaper(tp_id=tp_id, tp_question_no=tp_question_no, tp_question_text=tp_question_text, tp_question_total_mark=tp_question_total_mark)
        db.session.add(insert)
        db.session.commit()
        return 0
    
    @staticmethod
    def add_to_skill_testpaper(tp_id, tp_question_no, sk_id):
        insert = Skill_TestPaper(tp_id=tp_id, tp_question_no=tp_question_no, sk_id=sk_id)
        db.session.add(insert)
        db.session.commit()
        return 0
    
    @staticmethod
    def get_sk_id_by_name(sk_name):
        return Skill.query.filter(Skill.sk_name==sk_name).first()
    

    @staticmethod
    def set_student_mark(cl_id: str, tp_id: int, tp_question_no:int, s_id:int, norm_mark:float = 0):
        test_result = DBHandler.get_test_result(cl_id, tp_id, tp_question_no, s_id)

        if test_result == 0 or test_result is None:
            test_result = Test_Result(cl_id=cl_id, tp_id=tp_id, tp_question_no=tp_question_no, s_id=s_id)
            db.session.add(test_result)

        test_result.set_student_mark(norm_mark)

        db.session.commit()

    @staticmethod
    def upload_file(filename, data):
        insert = PDF_upload(filename=filename, data=data)
        db.session.add(insert)
        db.session.commit()


    @staticmethod
    def get_file(filename):
        output = PDF_upload.query.filter(PDF_upload.filename==filename).first().data
        return output
