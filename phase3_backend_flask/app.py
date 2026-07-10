from flask import Flask, request, jsonify
from database import get_connection
import math

app = Flask(__name__)

# -------------------------------------------------------
# GET COURSES BY DEPARTMENT AND SEMESTER
# -------------------------------------------------------

@app.route("/courses/<dept>/<int:semester>", methods=["GET"])
def get_courses(dept, semester):
    conn = get_connection()
    core = conn.execute("""
        SELECT course_id, course_name, credits FROM courses
        WHERE semester=? AND type='core' AND (department=? OR department='ALL')
    """, (semester, dept)).fetchall()
    elective = conn.execute("""
        SELECT course_id, course_name, credits FROM courses
        WHERE semester=? AND type='elective'
    """, (semester,)).fetchall()
    conn.close()
    return jsonify({"core": [dict(r) for r in core], "elective": [dict(r) for r in elective]})


# -------------------------------------------------------
# REGISTER STUDENT
# -------------------------------------------------------

@app.route("/register_student", methods=["POST"])
def register_student():
    data = request.json
    name, roll, department, semester, courses = data["name"], data["roll"], data["department"], data["semester"], data["courses"]
    conn = get_connection()
    semester_rules = {1:(18,2),2:(18,5),3:(21,5),4:(21,5),5:(22,6),6:(21,6),7:(11,2),8:(8,2)}
    max_credit, max_elective = semester_rules[semester]
    placeholders = ",".join(["?"] * len(courses))
    rows = conn.execute(f"SELECT type, credits FROM courses WHERE course_id IN ({placeholders})", courses).fetchall()
    total_credit = elective_credit = 0
    for r in rows:
        total_credit += r["credits"]
        if r["type"] == "elective": elective_credit += r["credits"]
    if total_credit > max_credit:
        conn.close(); return jsonify({"error": "Total semester credit limit exceeded"}), 400
    if elective_credit > max_elective:
        conn.close(); return jsonify({"error": "Elective credit limit exceeded"}), 400
    conn.execute("INSERT OR IGNORE INTO students(name,roll,department) VALUES(?,?,?)", (name,roll,department))
    for c in courses:
        conn.execute("INSERT INTO student_courses(student_roll,course_id) VALUES(?,?)", (roll,c))
    conn.commit(); conn.close()
    return jsonify({"message": "Courses registered successfully"})


# -------------------------------------------------------
# VIEW STUDENTS
# -------------------------------------------------------

@app.route("/students", methods=["GET"])
def students():
    conn = get_connection()
    data = conn.execute("""
        SELECT s.name, s.roll, s.department, GROUP_CONCAT(c.course_name, ', ') AS course_name
        FROM students s JOIN student_courses sc ON s.roll=sc.student_roll
        JOIN courses c ON c.course_id=sc.course_id GROUP BY s.roll ORDER BY s.department
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in data])



# -------------------------------------------------------
# VIEW STUDENTS — filtered by dept + batch prefix + semester
# -------------------------------------------------------

@app.route("/students/<dept>/<batch>/<int:semester>", methods=["GET"])
def students_filtered(dept, batch, semester):
    """
    Returns students in `dept` whose roll starts with `batch` (2-digit year)
    and who are registered in courses belonging to `semester`.
    Only courses of that semester are included in course_name.
    """
    conn = get_connection()
    data = conn.execute("""
        SELECT s.name, s.roll, s.department,
               GROUP_CONCAT(c.course_name, ', ') AS course_name
        FROM students s
        JOIN student_courses sc ON s.roll = sc.student_roll
        JOIN courses c          ON c.course_id = sc.course_id
        WHERE s.department      = ?
          AND SUBSTR(s.roll, 1, 2) = ?
          AND c.semester        = ?
        GROUP BY s.roll
        ORDER BY s.roll
    """, (dept, batch, semester)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in data])


# -------------------------------------------------------
# ANALYTICS
# -------------------------------------------------------

@app.route("/analytics", methods=["GET"])
def analytics():
    conn = get_connection()
    data = conn.execute("SELECT department, COUNT(*) as total_students FROM students GROUP BY department").fetchall()
    conn.close()
    return jsonify([dict(r) for r in data])


# -------------------------------------------------------
# ENSURE TABLES HELPER
# -------------------------------------------------------

def ensure_marks_tables(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS exam_components (
        id INTEGER PRIMARY KEY AUTOINCREMENT, course_id INTEGER,
        component_name TEXT, max_marks INTEGER,
        FOREIGN KEY(course_id) REFERENCES courses(course_id))""")
    conn.execute("""CREATE TABLE IF NOT EXISTS student_marks (
        id INTEGER PRIMARY KEY AUTOINCREMENT, student_roll TEXT,
        course_id INTEGER, component_id INTEGER, marks REAL,
        FOREIGN KEY(student_roll) REFERENCES students(roll),
        FOREIGN KEY(course_id) REFERENCES courses(course_id),
        FOREIGN KEY(component_id) REFERENCES exam_components(id))""")
    conn.commit()


# -------------------------------------------------------
# TEACHERS API — List teachers (filter by dept)
# -------------------------------------------------------

@app.route("/teachers", methods=["GET"])
def get_teachers():
    dept = request.args.get("dept")
    conn = get_connection()
    if dept:
        rows = conn.execute("SELECT teacher_id, teacher_name, department FROM teachers WHERE department=? ORDER BY teacher_name", (dept,)).fetchall()
    else:
        rows = conn.execute("SELECT teacher_id, teacher_name, department FROM teachers ORDER BY department, teacher_name").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# -------------------------------------------------------
# TEACHERS API — Courses assigned to a specific teacher
# -------------------------------------------------------

@app.route("/teacher/<int:teacher_id>/courses", methods=["GET"])
def get_teacher_courses(teacher_id):
    conn = get_connection()
    rows = conn.execute("""
        SELECT c.course_id, c.course_code, c.course_name, c.credits, c.semester, c.department
        FROM teacher_courses tc JOIN courses c ON tc.course_id=c.course_id
        WHERE tc.teacher_id=? ORDER BY c.semester, c.course_code
    """, (teacher_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# -------------------------------------------------------
# EXAM COMPONENTS — Get components for a course
# -------------------------------------------------------

@app.route("/exam_components/<int:course_id>", methods=["GET"])
def get_exam_components(course_id):
    conn = get_connection()
    ensure_marks_tables(conn)
    rows = conn.execute("SELECT id, component_name, max_marks FROM exam_components WHERE course_id=? ORDER BY id", (course_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# -------------------------------------------------------
# EXAM COMPONENTS — Save/replace components for a course
# -------------------------------------------------------

@app.route("/exam_components/<int:course_id>", methods=["POST"])
def save_exam_components(course_id):
    data = request.json
    teacher_id = data.get("teacher_id")
    components = data.get("components", [])
    total = sum(c["max_marks"] for c in components)
    if total != 100:
        return jsonify({"error": f"Component marks must sum to 100. Currently: {total}"}), 400
    conn = get_connection()
    owns = conn.execute("SELECT 1 FROM teacher_courses WHERE teacher_id=? AND course_id=?", (teacher_id, course_id)).fetchone()
    if not owns:
        conn.close(); return jsonify({"error": "Teacher not authorized for this course"}), 403
    ensure_marks_tables(conn)
    old_ids = conn.execute("SELECT id FROM exam_components WHERE course_id=?", (course_id,)).fetchall()
    for row in old_ids:
        conn.execute("DELETE FROM student_marks WHERE component_id=?", (row["id"],))
    conn.execute("DELETE FROM exam_components WHERE course_id=?", (course_id,))
    for comp in components:
        conn.execute("INSERT INTO exam_components (course_id, component_name, max_marks) VALUES (?,?,?)",
                     (course_id, comp["name"], comp["max_marks"]))
    conn.commit(); conn.close()
    return jsonify({"message": "Components saved successfully"})


# -------------------------------------------------------
# STUDENT MARKS — Get marks for a course
# -------------------------------------------------------

@app.route("/marks/<int:course_id>", methods=["GET"])
def get_marks(course_id):
    conn = get_connection()
    ensure_marks_tables(conn)
    students_in_course = conn.execute("""
        SELECT s.roll, s.name FROM students s JOIN student_courses sc ON s.roll=sc.student_roll
        WHERE sc.course_id=? ORDER BY s.roll
    """, (course_id,)).fetchall()
    marks_rows = conn.execute("SELECT student_roll, component_id, marks FROM student_marks WHERE course_id=?", (course_id,)).fetchall()
    conn.close()
    marks_lookup = {}
    for m in marks_rows:
        roll = m["student_roll"]
        if roll not in marks_lookup: marks_lookup[roll] = {}
        marks_lookup[roll][str(m["component_id"])] = m["marks"]
    result = [{"roll": s["roll"], "name": s["name"], "marks": marks_lookup.get(s["roll"], {})} for s in students_in_course]
    return jsonify(result)


# -------------------------------------------------------
# STUDENT MARKS — Save/update marks
# -------------------------------------------------------

@app.route("/marks/<int:course_id>", methods=["POST"])
def save_marks(course_id):
    data = request.json
    teacher_id = data.get("teacher_id")
    marks_data = data.get("marks", [])
    conn = get_connection()
    owns = conn.execute("SELECT 1 FROM teacher_courses WHERE teacher_id=? AND course_id=?", (teacher_id, course_id)).fetchone()
    if not owns:
        conn.close(); return jsonify({"error": "Teacher not authorized"}), 403
    ensure_marks_tables(conn)
    for entry in marks_data:
        roll, comp_id, mark_val = entry["roll"], entry["component_id"], entry["marks"]
        comp_row = conn.execute("SELECT max_marks FROM exam_components WHERE id=?", (comp_id,)).fetchone()
        if comp_row and mark_val > comp_row["max_marks"]:
            conn.close(); return jsonify({"error": f"Marks exceed max for component {comp_id}"}), 400
        existing = conn.execute("SELECT id FROM student_marks WHERE student_roll=? AND course_id=? AND component_id=?", (roll, course_id, comp_id)).fetchone()
        if existing:
            conn.execute("UPDATE student_marks SET marks=? WHERE student_roll=? AND course_id=? AND component_id=?", (mark_val, roll, course_id, comp_id))
        else:
            conn.execute("INSERT INTO student_marks (student_roll,course_id,component_id,marks) VALUES (?,?,?,?)", (roll, course_id, comp_id, mark_val))
    conn.commit(); conn.close()
    return jsonify({"message": "Marks saved successfully"})


# -------------------------------------------------------
# ANALYTICS — Student Academic Record
# -------------------------------------------------------

@app.route("/student_record/<roll>", methods=["GET"])
def get_student_record(roll):
    conn = get_connection()
    ensure_marks_tables(conn)
    student = conn.execute("SELECT roll, name, department FROM students WHERE roll=?", (roll,)).fetchone()
    if not student:
        conn.close(); return jsonify({"error": "Student not found"}), 404

    semesters = conn.execute("""
        SELECT DISTINCT c.semester FROM student_courses sc
        JOIN courses c ON sc.course_id=c.course_id WHERE sc.student_roll=? ORDER BY c.semester
    """, (roll,)).fetchall()

    def z_to_grade(z):
        if z >= 1.5: return "A", 10
        elif z >= 1.0: return "A-", 9
        elif z >= 0.5: return "B", 8
        elif z >= 0.0: return "B-", 7
        elif z >= -0.5: return "C", 6
        elif z >= -1.0: return "C-", 5
        else: return "D", 4

    semester_records = []
    cgpa_progression = []
    total_credits_so_far = 0
    weighted_gp_so_far = 0

    for sem_row in semesters:
        sem = sem_row["semester"]
        student_courses_sem = conn.execute("""
            SELECT c.course_id, c.course_code, c.course_name, c.credits
            FROM student_courses sc JOIN courses c ON sc.course_id=c.course_id
            WHERE sc.student_roll=? AND c.semester=?
        """, (roll, sem)).fetchall()

        courses_detail = []
        sem_credits = 0
        sem_weighted_gp = 0
        has_marks = False

        for course in student_courses_sem:
            cid = course["course_id"]
            components = conn.execute("SELECT id, component_name, max_marks FROM exam_components WHERE course_id=? ORDER BY id", (cid,)).fetchall()

            if not components:
                courses_detail.append({"course_code": course["course_code"], "course_name": course["course_name"],
                                        "credits": course["credits"], "total_marks": None, "grade": "—", "grade_points": None})
                continue

            my_marks = conn.execute("SELECT component_id, marks FROM student_marks WHERE student_roll=? AND course_id=?", (roll, cid)).fetchall()
            my_marks_dict = {m["component_id"]: m["marks"] for m in my_marks}
            my_total = sum(my_marks_dict.get(c["id"], 0) for c in components)

            # Get all students in this course for z-score
            all_students = conn.execute("SELECT DISTINCT student_roll FROM student_marks WHERE course_id=?", (cid,)).fetchall()
            all_totals = []
            for st in all_students:
                st_roll = st["student_roll"]
                st_total = sum(
                    (conn.execute("SELECT marks FROM student_marks WHERE student_roll=? AND course_id=? AND component_id=?", (st_roll, cid, comp["id"])).fetchone() or {"marks": 0})["marks"]
                    for comp in components
                )
                all_totals.append(st_total)

            if len(all_totals) < 2:
                z = 0
            else:
                mean = sum(all_totals) / len(all_totals)
                variance = sum((x - mean) ** 2 for x in all_totals) / (len(all_totals))
                std_dev = math.sqrt(variance) if variance > 0 else 1
                z = (my_total - mean) / std_dev

            grade, gp = z_to_grade(z)
            has_marks = True
            sem_credits += course["credits"]
            sem_weighted_gp += gp * course["credits"]

            courses_detail.append({"course_code": course["course_code"], "course_name": course["course_name"],
                                    "credits": course["credits"], "total_marks": round(my_total, 2),
                                    "grade": grade, "grade_points": gp})

        sgpa = round(sem_weighted_gp / sem_credits, 2) if sem_credits > 0 and has_marks else None
        if sgpa is not None:
            total_credits_so_far += sem_credits
            weighted_gp_so_far += sem_weighted_gp
            cgpa = round(weighted_gp_so_far / total_credits_so_far, 2)
        else:
            cgpa = None

        semester_records.append({"semester": sem, "courses": courses_detail, "sgpa": sgpa, "cgpa_after": cgpa})
        if cgpa is not None:
            cgpa_progression.append({"semester": sem, "cgpa": cgpa})

    conn.close()
    return jsonify({"roll": student["roll"], "name": student["name"], "department": student["department"],
                    "semesters": semester_records, "cgpa_progression": cgpa_progression})


# -------------------------------------------------------
# RUN SERVER
# -------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=False)
