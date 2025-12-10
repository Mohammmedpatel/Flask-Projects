from flask import Flask, jsonify, request

app = Flask(__name__)

students = [
    {"id": 1, "Name": "Mohammed", "age": 22},
    {"id": 2, "Name": "MD", "age": 20},
    {"id": 3, "Name": "Mustakeem", "age": 21}
]

@app.route("/")
def home():
    return "Hello Flask!"

@app.route("/students", methods=["GET"])
def read_all():
    return jsonify(students)

@app.route("/students/<int:id>", methods=["GET"])
def featch_detail(id):  
    for i in students:
        if i["id"] == id:
            return jsonify(i)
    return "Student not found"
 
@app.route("/students", methods=["POST"]) 
def add_student():
    student_deatils=request.get_json()
    new_student_id=students[-1]["id"]+1
    student_deatils["id"]=new_student_id
    students.append(student_deatils)
    return "Successfully added"

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_stu(student_id):
    update_detail=request.get_json()
    for i in students:
        if i["id"] == student_id:
            if update_detail.get("name"):
                i["Name"]=update_detail.get("name")
            if update_detail.get("age"):
                i["age"]=update_detail.get("age")
            return "Updated Successfully"
    return "Student Not Found" 


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_stu(student_id):
    for i in students:
        if i["id"] == student_id:
            students.remove(i)
            return "Deleted Successfully"
    return "Student Not Found"

if __name__ == "__main__":
    app.run(debug=True)

