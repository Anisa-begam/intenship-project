 defcalculate_student_grades(students):
    results = []

    for student in students:
        name = student["name"]
        marks = student["marks"]

        average = sum(marks) / len(marks)

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
            "name": name,
            "average": round(average, 2),
            "grade": grade
        })

    return results


# Input section
students = []

num_students = int(input("Enter number of students: "))

for i in range(num_students):
    print(f"\nStudent {i + 1}")

    name = input("Enter student name: ")

    marks = []
    num_subjects = int(input("Enter number of subjects: "))

    for j in range(num_subjects):
        mark = float(input(f"Enter mark for Subject {j + 1}: "))
        marks.append(mark)

    students.append({
        "name": name,
        "marks": marks
    })

# Calculate grades
results = calculate_student_grades(students)

# Display results
print("\n----- STUDENT GRADE REPORT -----")

for student in results:
    print(f"Name    : {student['name']}")
    print(f"Average : {student['average']}")
    print(f"Grade   : {student['grade']}")
    print("-" * 30)