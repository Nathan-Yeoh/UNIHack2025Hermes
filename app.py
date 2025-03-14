from flask import Flask, render_template, redirect, url_for, flash, request, session
#from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from datetime import datetime, timedelta

from db import db
from Entities.DBHandler import DBHandler
from Entities.Teacher import Teacher
from Entities.Classroom import Classroom
from Entities.Student_Classroom import Student_Classroom
from Entities.Student import Student
from Entities.Skill import Skill
from Entities.TestPaper import TestPaper
from Entities.Skill_TestPaper import Skill_TestPaper
from Entities.Test_Result import Test_Result
from Entities.Classroom_TestPaper import Classroom_TestPaper

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = "serve_login"  # redirect here if not logged in


db.init_app(app)

@app.route("/")
#@login_required
def serve_home():
    return render_template('Home.html')

@app.route("/Classroom", methods=["GET", "POST"])
def serve_classroom():
    return render_template('Classroom.html')

@app.route("/Classroom/Student", methods=["GET", "POST"])
def serve_student_graph():
    return render_template('StudentGraph.html')

@app.route("/Classroom/TestPaper", methods=["GET", "POST"])
def serve_testpaper():
    return render_template('TestPaper.html')

@app.route("/Classroom/TestPaper/Create")
def serve_testpaper_create():
    return render_template('TestPaperCreate.html')

@app.route("/Classroom/TestPaper/Edit")
def serve_testpaper_edit():
    return render_template('TestPaperEdit.html')

@app.route("/Classroom/TestPaper/Mark", methods=["GET", "POST"])
def serve_testpaper_mark():
    return render_template('TestPaperMark.html')

@app.route("/About")
def serve_about():
    return render_template('About.html')

@app.route("/Credit")
def serve_credit():
    return render_template('Credit.html')

with app.app_context():
    db.drop_all()
    db.create_all()
    
    Sankinator = Teacher(t_id=1, t_username='MrSankey')
    Tan = Teacher(t_id=2, t_username="MrTan")
    db.session.add(Sankinator)
    db.session.add(Tan)

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
    class2 = Classroom(cl_id='FIT1012', t_id=2)
    db.session.add(class1)
    db.session.add(class2)

    cAdam =  Student_Classroom(cl_id='FIT1049', s_id=1)
    cWroe =  Student_Classroom(cl_id='FIT1049', s_id=2)
    cSmart = Student_Classroom(cl_id='FIT1049', s_id=3)
    cPant =  Student_Classroom(cl_id='FIT1012', s_id=4)
    cKoolaid = Student_Classroom(cl_id='FIT1012', s_id=5)
    cHelp =  Student_Classroom(cl_id='FIT1012', s_id=6)
    db.session.add(cAdam)
    db.session.add(cWroe)
    db.session.add(cSmart)
    db.session.add(cPant)
    db.session.add(cKoolaid)
    db.session.add(cHelp)

    #Please replace these im very tired and cant think of good skills. like how tf u write a question about communication?
    Creativity = Skill(sk_id=1, sk_name='Creativity', sk_desc='Lorem Ipsum')
    Analytical = Skill(sk_id=2, sk_name='Analytical', sk_desc='Lorem Ipsum')
    Awareness = Skill(sk_id=3, sk_name='Awareness', sk_desc='Lorem Ipsum')
    Management = Skill(sk_id=4, sk_name='Management', sk_desc='Lorem Ipsum')
    Communication = Skill(sk_id=5, sk_name='Communication', sk_desc='Lorem Ipsum')
    db.session.add(Creativity)
    db.session.add(Analytical)
    db.session.add(Awareness)
    db.session.add(Management)
    db.session.add(Communication)

    db.session.commit() #Note: Teacher, Student, Skills, Classroom, and Student_Classroom data creation is assumed out of scope!




if __name__ == "__main__":
    app.run(debug=True)