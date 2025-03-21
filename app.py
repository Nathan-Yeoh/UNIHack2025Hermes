from flask import Flask, render_template, request, jsonify, redirect, url_for

from OpenaiHandler import OpenaiHandler
from DBHandler import DBHandler
from Entities.Classroom import Classroom
from Entities.Classroom_TestPaper import Classroom_TestPaper
from Entities.Skill import Skill
from Entities.Skill_TestPaper import Skill_TestPaper
from Entities.Student import Student
from Entities.Student_Classroom import Student_Classroom
from Entities.Teacher import Teacher
from Entities.TestPaper import TestPaper
from Entities.Test_Result import Test_Result
from db import db

# from flask_login import LoginManager, login_user, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "serve_login"  # redirect here if not logged in


db.init_app(app)


@app.route("/")
# @login_required
def serve_home():
    classroom = DBHandler.get_classroom_by_teacher(t_id=1)
    return render_template('Home.html', classroom=classroom)

    # if request.method == "POST": # this is going to run after making a new classroom
    #     classroom = Classroom()
    #     classroom.name = request.form.get("classroomName")
    #     DBHandler.addClassroom(classroom)
    #
    # all_classrooms = DBHandler.getAllClassrooms()
    # return render_template('Home.html', all_classrooms = all_classrooms)


# API route to provide chart data
@app.route('/chart-data')
def chart_data():
    # student = DBHandler.getStudentFromId(s_id=s_id) TODO this ?might? be used to make radar chart
    data = {
        "labels": ["Speed", "Strength", "Agility", "Endurance", "Flexibility"],
        "datasets": [
            {
                "label": "Athlete A",
                "data": [80, 90, 75, 85, 70],
                "backgroundColor": "rgba(54, 162, 235, 0.2)",
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 2
            },
            {
                "label": "Athlete B",
                "data": [60, 85, 95, 70, 80],
                "backgroundColor": "rgba(255, 99, 132, 0.2)",
                "borderColor": "rgba(255, 99, 132, 1)",
                "borderWidth": 2
            }
        ]
    }
    return jsonify(data)


@app.route("/Classroom/<string:cl_id>", methods=["GET", "POST"])
def serve_classroom(cl_id: str):
    if request.method == "POST":
        # get the classroom ID
        cl_id = request.form.get("cl_id")

    # get all test papers from this classroom
    test_papers = DBHandler.get_testpapers_by_classroom(cl_id)
    # get all students in this classroom
    students = DBHandler.get_students_by_classroom(cl_id)

    return render_template('Classroom.html', cl_id=cl_id, test_papers=test_papers, students=students, all_testpapers=DBHandler.get_all_tp())


@app.route("/Classroom/Student", methods=["GET", "POST"])
def serve_student_graph():
    if request.method == "POST":
        s_id = request.form.get("s_id")
        cl_id = request.form.get("cl_id")
        print(cl_id)
    skillnames = DBHandler.get_all_skill_names()
    student = DBHandler.get_student_by_id(s_id=s_id)
    studattributes, attributes = DBHandler.get_attribute_values(s_id=s_id, cl_id=cl_id)
    return render_template('StudentGraph.html', skillnames=skillnames, student=student, studattributes=studattributes, attributes=attributes, classroom_id=cl_id)


@app.route("/Classroom/TestPaper/<string:cl_id>/<int:tp_id>", methods=["GET", "POST"])
def serve_testpaper(cl_id: str, tp_id: int):
    students = DBHandler.get_students_by_classroom(cl_id)
    classroom_testpaper = DBHandler.get_testpaper_by_cltp_id(cl_id, tp_id)
    return render_template('TestPaper.html', cl_id=cl_id, students=students, classroom_testpaper=classroom_testpaper)


@app.route("/Classroom/TestPaper/Create", methods=["GET", "POST"])
def serve_testpaper_create(cl_id = None, tp_id=None):
    if request.method == "POST":
        # class and test id
        cl_id = request.form.get("cl_id")
        tp_id = request.form.get("tp_id")


    return render_template('TestPaperCreate.html', cl_id=cl_id, tp_id=tp_id)


@app.route("/Classroom/TestPaper/Edit/<string:cl_id>/<int:tp_id>", methods=["GET", "POST"])
def serve_testpaper_edit(cl_id: str, tp_id: int):
    if request.method == "POST":
        cl_id = request.form.get("cl_id")
        tp_id = int(request.form.get("tp_id"))
        tp_name = request.form.get("tp_name")

        try:
            tp_file = request.files['tp_file']
            DBHandler.upload_file(tp_file.filename, tp_file.read())
            OpenaiHandler.insert_pdf_into_database(tp_file.filename, tp_id, cl_id, tp_name)
        except:
            pass
        
    classroom_testpaper = DBHandler.get_testpaper_by_cltp_id(cl_id, tp_id)

    # get the questions of the test as a tuple (question string, marks available)
    questions = DBHandler.get_testquestions_by_tp_id(tp_id)

    # get question attributes
    attributes = DBHandler.get_attribute_per_question(tp_id)

    return render_template('TestPaperEdit.html', classroom_testpaper=classroom_testpaper, questions=questions, attributes = attributes)

@app.route("/Classroom/TestPaper/Save/<string:cl_id>/<int:tp_id>", methods=["GET", "POST"])
def save_testpaper(cl_id: str, tp_id: int):
    if request.method == "POST":
        q_length = int(request.form.get("q_length"))
        for i in range(1, q_length+1):
            q_text = request.form.get(f"q_text{i}")
            q_marks = int(request.form.get(f"q_marks{i}"))
            DBHandler.update_testquestion_by_tp_question_id(tp_id, i, q_text, q_marks)

    return redirect(url_for("serve_classroom", cl_id=cl_id))

@app.route("/Classroom/TestPaper/Mark/<string:cl_id>/<int:tp_id>/<int:s_id>", methods=["GET", "POST"])
def serve_testpaper_mark(cl_id: str, tp_id: int, s_id: int):
    classroom_testpaper = DBHandler.get_testpaper_by_cltp_id(cl_id, tp_id)
    questions = DBHandler.get_testquestions_by_tp_id(tp_id)
    student = DBHandler.get_student_by_id(s_id)

    return render_template('TestPaperMark.html', classroom_testpaper=classroom_testpaper, questions=questions, student=student)


@app.route("/Classroom/TestPaper/Mark", methods=["GET", "POST"])
def mark_testpaper():
    if request.method == "POST":
        cl_id = request.form.get("cl_id")
        tp_id = int(request.form.get("tp_id"))
        s_id = int(request.form.get("s_id"))
        q_length = int(request.form.get("q_length"))

        for i in range(1, q_length+1):
            norm_mark = int(request.form.get(f"marks_given{i}")) / int(request.form.get(f"marks_avail{i}"))
            DBHandler.set_student_mark(cl_id, tp_id,i, s_id, norm_mark)

        return redirect(url_for("serve_classroom", cl_id=cl_id))

@app.route("/About")
def serve_about():
    return render_template('About.html')


@app.route("/Credits")
def serve_credit():
    return render_template('Credit.html')


with app.app_context():
    db.drop_all()
    db.create_all()

    Sankinator = Teacher(t_id=1, t_username='MrSankey')
    db.session.add(Sankinator)

    Adam = Student(s_id=1, s_name='Adam')
    Wroe = Student(s_id=2, s_name='Wroe')
    Smart = Student(s_id=3, s_name='Smart')
    Pant = Student(s_id=4, s_name='Pant')
    Koolaid = Student(s_id=5, s_name='Koolaid')
    Help = Student(s_id=6, s_name='Help')
    db.session.add(Adam)
    db.session.add(Wroe)
    db.session.add(Smart)
    db.session.add(Pant)
    db.session.add(Koolaid)
    db.session.add(Help)

    class1 = Classroom(cl_id='FIT1049', t_id=1)
    class2 = Classroom(cl_id='ENG1012', t_id=1)
    db.session.add(class1)
    db.session.add(class2)

    cAdam = Student_Classroom(cl_id='FIT1049', s_id=1)
    cWroe = Student_Classroom(cl_id='FIT1049', s_id=2)
    cSmart = Student_Classroom(cl_id='FIT1049', s_id=3)
    cPant = Student_Classroom(cl_id='ENG1012', s_id=4)
    cKoolaid = Student_Classroom(cl_id='ENG1012', s_id=5)
    cHelp = Student_Classroom(cl_id='ENG1012', s_id=6)
    db.session.add(cAdam)
    db.session.add(cWroe)
    db.session.add(cSmart)
    db.session.add(cPant)
    db.session.add(cKoolaid)
    db.session.add(cHelp)

    # Please replace these im very tired and cant think of good skills. like how tf u write a question about communication?
    skill1 = Skill(sk_id=1, sk_name='Creativity', sk_desc='Lorem Ipsum')
    skill2 = Skill(sk_id=2, sk_name='Logical Reasoning', sk_desc='Lorem Ipsum')
    skill3 = Skill(sk_id=3, sk_name='Perception', sk_desc='Lorem Ipsum')
    skill4 = Skill(sk_id=4, sk_name='Memory', sk_desc='Lorem Ipsum')
    skill5 = Skill(sk_id=5, sk_name='Language', sk_desc='Lorem Ipsum')
    skill6 = Skill(sk_id=6, sk_name='Adaptability', sk_desc='Lorem Ipsum')
    skill7 = Skill(sk_id=7, sk_name='Application', sk_desc='Lorem Ipsum')
    skill8 = Skill(sk_id=8, sk_name='Problem Solving', sk_desc='Lorem Ipsum')

    db.session.add(skill1)
    db.session.add(skill2)
    db.session.add(skill3)
    db.session.add(skill4)
    db.session.add(skill5)
    db.session.add(skill6)
    db.session.add(skill7)
    db.session.add(skill8)

    db.session.commit()  # Note: Teacher, Student, Skills, Classroom, and Student_Classroom data creation is assumed out of scope!

    


if __name__ == "__main__":
    app.run(debug=True)
