from flask import Flask , render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///SMS.db"
app.config["UPLOAD_FOLDER"]="static/upload"
db=SQLAlchemy(app)

class Student(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30), nullable=False)
    email=db.Column(db.String(30), nullable=False, unique=True)
    dob=db.Column(db.String(30), nullable=False)
    gender=db.Column(db.String(8),nullable=False)
    roll_no=db.Column(db.String(5),nullable=False)
    Addmission_date=db.Column(db.Date, nullable=False)
    course=db.Column(db.String(15),nullable=False)
    photo=db.Column(db.String(50),nullable=False)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    students=Student.query.all()
    return render_template("index.html",students=students)

@app.route("/add_student",methods=["GET","POST"])
def add_stu():
    if request.method=="POST":
        name =  request.form.get("name")
        email =  request.form.get("email")
        dob =  request.form.get("dob")
        dob = datetime.strptime(dob,"%Y-%m-%d").date()
        gender =  request.form.get("gender")
        rollno =  request.form.get("rollno")
        admission =  request.form.get("admission")
        admission = datetime.strptime(admission,"%Y-%m-%d").date()
        course =  request.form.get("course")

        photo =  request.files["photo"]
        photo_path=os.path.join(app.config["UPLOAD_FOLDER"],photo.filename)
        photo.save(photo_path)

        student=Student(name=name, email=email, dob=dob, gender=gender, roll_no=rollno, Addmission_date=admission, course=course, photo=photo.filename)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for("home"))
        print({"name":name,"email":email,"dob":dob,"gender":gender,"rollno":rollno,"admission":admission,"course":course,"photo":photo})
    return render_template("add_student.html")

@app.route("/student_detail/<int:student_id>",methods=["GET"])
def student_detail(student_id):
    students=Student.query.get(student_id)
    return render_template("student_detail.html",students=students)

@app.route("/update_student/<int:student_id>",methods=["GET","POST"])
def update_student(student_id):
    students=Student.query.get(student_id)
    if request.method=="POST":
        students.name =  request.form.get("name")
        students.email =  request.form.get("email")
        dob =  request.form.get("dob")
        students.dob = datetime.strptime(dob,"%Y-%m-%d").date()
        students.gender =  request.form.get("gender")
        students.rollno =  request.form.get("rollno")
        admission =  request.form.get("admission")
        students.admission = datetime.strptime(admission,"%Y-%m-%d").date()
        students.course =  request.form.get("course")

        photo =  request.files["photo"]
        photo_path=os.path.join(app.config["UPLOAD_FOLDER"],photo.filename)
        photo.save(photo_path)
        students.photo=photo.filename
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("update_student.html",students=students)

@app.route("/delete_student/<int:student_id>",methods=["GET","POST"])
def delete_student(student_id):
    students=Student.query.get(student_id)
    db.session.delete(students)
    db.session.commit()
    return redirect(url_for("home"))

if __name__=="__main__":
    app.run(debug=True)