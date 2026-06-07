from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def calculate_student_grades(students):
    results = []

    for student in students:
        average = sum(student["marks"]) / len(student["marks"])

        if average >= 95:
            grade = "A+"
        elif average >= 90:
            grade = "A"
        elif average >= 75:
            grade = "B"
        elif average >= 60:
            grade = "C"
        else:
            grade = "D"

        results.append({
            "name": student["name"],
            "average": round(average, 2),
            "grade": grade
        })

    return results

@app.route("/")
def index():
    return render_template("my_ui.html")

@app.route("/my-ui")
def my_ui():
    return render_template("my_ui.html")

@app.route("/calculate-grades", methods=["POST"])
def calculate_grades():
    data = request.get_json()
    students = data["students"]

    result = calculate_student_grades(students)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
