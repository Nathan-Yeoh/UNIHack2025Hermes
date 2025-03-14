from flask import Flask, render_template, redirect, url_for, flash, request, session
#from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from datetime import datetime, timedelta

from db import db

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

if __name__ == "__main__":
    app.run(debug=True)