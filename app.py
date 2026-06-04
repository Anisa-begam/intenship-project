from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

def calculate_grade(average):
    if average >= 90:
        return 'A'
    elif average >= 80:
        return 'B'
    elif average >= 70:
        return 'C'
    elif average >= 60:
        return 'D'
    elif average >= 50:
        return 'E'
    else:
        return 'F'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    students = data.get('students', [])
    
    results = []
    for student in students:
        name = student.get('name', '')
        marks = student.get('marks', [])
        
        if marks:
            average = sum(marks) / len(marks)
            grade = calculate_grade(average)
        else:
            average = 0
            grade = 'N/A'
        
        results.append({
            "name": name,
            "average": round(average, 2),
            "grade": grade
        })
    
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
