DROP TABLE IF EXISTS student_courses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS teacher_courses;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS courses;

---

-- STUDENTS TABLE

CREATE TABLE students(
roll VARCHAR(10) PRIMARY KEY,
name TEXT,
department TEXT
);

---

-- COURSES TABLE

CREATE TABLE courses(
course_id INTEGER PRIMARY KEY AUTOINCREMENT,
course_code TEXT,
course_name TEXT,
department TEXT,
semester INTEGER,
type TEXT,
credits INTEGER
);

---

-- STUDENT COURSES

CREATE TABLE student_courses(
id INTEGER PRIMARY KEY AUTOINCREMENT,
student_roll TEXT,
course_id INTEGER,
FOREIGN KEY(student_roll) REFERENCES students(roll),
FOREIGN KEY(course_id) REFERENCES courses(course_id)
);

---

-- SEMESTER 1

INSERT INTO courses(course_code,course_name,department,semester,type,credits) VALUES
('CSE101','Programming Fundamentals','CSE',1,'core',4),
('CSE102','Engineering Mathematics I','CSE',1,'core',4),
('CSE103','Engineering Physics','CSE',1,'core',3),
('CSE104','Basic Electrical Engineering','CSE',1,'core',3),
('CSE105','Engineering Workshop','CSE',1,'core',2),

('DSAI101','Introduction to Data Science','DSAI',1,'core',4),
('DSAI102','Engineering Mathematics I','DSAI',1,'core',4),
('DSAI103','Statistics Fundamentals','DSAI',1,'core',3),
('DSAI104','Programming Fundamentals','DSAI',1,'core',3),
('DSAI105','Data Science Lab','DSAI',1,'core',2),

('ECE101','Engineering Physics','ECE',1,'core',4),
('ECE102','Basic Electronics','ECE',1,'core',4),
('ECE103','Engineering Mathematics I','ECE',1,'core',3),
('ECE104','Engineering Mechanics','ECE',1,'core',3),
('ECE105','Workshop Practice','ECE',1,'core',2);

INSERT INTO courses VALUES
(NULL,'ELE101','Creative Thinking','ALL',1,'elective',2),
(NULL,'ELE102','Technical Writing','ALL',1,'elective',2),
(NULL,'ELE103','Environmental Studies','ALL',1,'elective',1),
(NULL,'ELE104','Ethics in Engineering','ALL',1,'elective',1);

---

-- SEMESTER 2

INSERT INTO courses VALUES
(NULL,'CSE201','Data Structures','CSE',2,'core',4),
(NULL,'CSE202','Discrete Mathematics','CSE',2,'core',4),
(NULL,'CSE203','Computer Organization','CSE',2,'core',3),
(NULL,'CSE204','Object Oriented Programming','CSE',2,'core',3),
(NULL,'CSE205','Programming Lab','CSE',2,'core',2),

(NULL,'DSAI201','Python Programming','DSAI',2,'core',4),
(NULL,'DSAI202','Probability Theory','DSAI',2,'core',4),
(NULL,'DSAI203','Linear Algebra','DSAI',2,'core',3),
(NULL,'DSAI204','Data Visualization','DSAI',2,'core',3),
(NULL,'DSAI205','Python Lab','DSAI',2,'core',2),

(NULL,'ECE201','Signals and Systems','ECE',2,'core',4),
(NULL,'ECE202','Analog Electronics','ECE',2,'core',4),
(NULL,'ECE203','Network Theory','ECE',2,'core',3),
(NULL,'ECE204','Digital Logic','ECE',2,'core',3),
(NULL,'ECE205','Electronics Lab','ECE',2,'core',2);

INSERT INTO courses VALUES
(NULL,'ELE201','Cyber Security Basics','ALL',2,'elective',2),
(NULL,'ELE202','Cloud Computing Fundamentals','ALL',2,'elective',2),
(NULL,'ELE203','Communication Skills','ALL',2,'elective',1),
(NULL,'ELE204','Innovation & Design','ALL',2,'elective',1);

---

-- SEMESTER 3

INSERT INTO courses VALUES
(NULL,'CSE301','Operating Systems','CSE',3,'core',4),
(NULL,'CSE302','Database Systems','CSE',3,'core',4),
(NULL,'CSE303','Software Engineering','CSE',3,'core',3),
(NULL,'CSE304','Computer Networks','CSE',3,'core',3),
(NULL,'CSE305','DBMS Lab','CSE',3,'core',2),

(NULL,'DSAI301','Machine Learning','DSAI',3,'core',4),
(NULL,'DSAI302','Data Mining','DSAI',3,'core',4),
(NULL,'DSAI303','Statistical Modeling','DSAI',3,'core',3),
(NULL,'DSAI304','Big Data Fundamentals','DSAI',3,'core',3),
(NULL,'DSAI305','ML Lab','DSAI',3,'core',2),

(NULL,'ECE301','Digital Electronics','ECE',3,'core',4),
(NULL,'ECE302','Microprocessors','ECE',3,'core',4),
(NULL,'ECE303','Control Systems','ECE',3,'core',3),
(NULL,'ECE304','Communication Systems','ECE',3,'core',3),
(NULL,'ECE305','Microprocessor Lab','ECE',3,'core',2);

INSERT INTO courses VALUES
(NULL,'ELE301','Blockchain Basics','ALL',3,'elective',2),
(NULL,'ELE302','IoT Fundamentals','ALL',3,'elective',2),
(NULL,'ELE303','Technical Presentation','ALL',3,'elective',1),
(NULL,'ELE304','Entrepreneurship','ALL',3,'elective',1);

---

-- SEMESTER 4

INSERT INTO courses VALUES
(NULL,'CSE401','Compiler Design','CSE',4,'core',4),
(NULL,'CSE402','Artificial Intelligence','CSE',4,'core',4),
(NULL,'CSE403','Computer Graphics','CSE',4,'core',3),
(NULL,'CSE404','Theory of Computation','CSE',4,'core',3),
(NULL,'CSE405','Mini Project','CSE',4,'core',2),

(NULL,'DSAI401','Deep Learning','DSAI',4,'core',4),
(NULL,'DSAI402','Natural Language Processing','DSAI',4,'core',4),
(NULL,'DSAI403','Data Warehousing','DSAI',4,'core',3),
(NULL,'DSAI404','Data Security And Privacy','DSAI',4,'core',3),
(NULL,'DSAI405','Big Data Analytics','DSAI',4,'core',2),

(NULL,'ECE401','VLSI Design','ECE',4,'core',4),
(NULL,'ECE402','Embedded Systems','ECE',4,'core',4),
(NULL,'ECE403','Digital Signal Processing','ECE',4,'core',3),
(NULL,'ECE404','Wireless Communication','ECE',4,'core',3),
(NULL,'ECE405','VLSI Lab','ECE',4,'core',2);

INSERT INTO courses VALUES
(NULL,'ELE401','AR/VR Basics','ALL',4,'elective',2),
(NULL,'ELE402','Mobile App Development','ALL',4,'elective',2),
(NULL,'ELE403','Professional Ethics','ALL',4,'elective',1),
(NULL,'ELE404','Research Methodology','ALL',4,'elective',1);

---

-- SEMESTER 5

INSERT INTO courses VALUES
(NULL,'CSE501','Advanced Algorithms','CSE',5,'core',4),
(NULL,'CSE502','Distributed Systems','CSE',5,'core',4),
(NULL,'CSE503','Cloud Computing','CSE',5,'core',3),
(NULL,'CSE504','Cyber Security','CSE',5,'core',3),
(NULL,'CSE505','Cloud Lab','CSE',5,'core',2),

(NULL,'DSAI501','Advanced Machine Learning','DSAI',5,'core',4),
(NULL,'DSAI502','AI Systems','DSAI',5,'core',4),
(NULL,'DSAI503','Data Ethics','DSAI',5,'core',3),
(NULL,'DSAI504','Reinforcement Learning','DSAI',5,'core',3),
(NULL,'DSAI505','AI Lab','DSAI',5,'core',2),

(NULL,'ECE501','Satellite Communication','ECE',5,'core',4),
(NULL,'ECE502','RF Engineering','ECE',5,'core',4),
(NULL,'ECE503','Robotics','ECE',5,'core',3),
(NULL,'ECE504','Advanced Embedded Systems','ECE',5,'core',3),
(NULL,'ECE505','Robotics Lab','ECE',5,'core',2);

INSERT INTO courses VALUES
(NULL,'ELE501','Game Development','ALL',5,'elective',2),
(NULL,'ELE502','Quantum Computing Basics','ALL',5,'elective',2),
(NULL,'ELE503','Digital Marketing','ALL',5,'elective',1),
(NULL,'ELE504','Innovation Management','ALL',5,'elective',1);

---

-- SEMESTER 6

INSERT INTO courses VALUES
(NULL,'CSE601','Parallel Computing','CSE',6,'core',4),
(NULL,'CSE602','Advanced Database Systems','CSE',6,'core',4),
(NULL,'CSE603','Web Engineering','CSE',6,'core',3),
(NULL,'CSE604','Information Retrieval','CSE',6,'core',3),
(NULL,'CSE605','Web Lab','CSE',6,'core',2),

(NULL,'DSAI601','AI Ethics','DSAI',6,'core',4),
(NULL,'DSAI602','Advanced Analytics','DSAI',6,'core',4),
(NULL,'DSAI603','Recommendation Systems','DSAI',6,'core',3),
(NULL,'DSAI604','Graph Mining','DSAI',6,'core',3),
(NULL,'DSAI605','Analytics Lab','DSAI',6,'core',2),

(NULL,'ECE601','Optical Communication','ECE',6,'core',4),
(NULL,'ECE602','Advanced DSP','ECE',6,'core',4),
(NULL,'ECE603','Nano Electronics','ECE',6,'core',3),
(NULL,'ECE604','Autonomous Systems','ECE',6,'core',3),
(NULL,'ECE605','DSP Lab','ECE',6,'core',2);

INSERT INTO courses VALUES
(NULL,'ELE601','Human Computer Interaction','ALL',6,'elective',2),
(NULL,'ELE602','FinTech Basics','ALL',6,'elective',2),
(NULL,'ELE603','Design Thinking','ALL',6,'elective',1),
(NULL,'ELE604','Leadership Skills','ALL',6,'elective',1);

---

-- SEMESTER 7

INSERT INTO courses VALUES
(NULL,'GEN701','Industry Internship','ALL',7,'core',6),
(NULL,'GEN702','Major Project Phase I','ALL',7,'core',3);

INSERT INTO courses VALUES
(NULL,'ELE701','Startup Management','ALL',7,'elective',1),
(NULL,'ELE702','Patent Writing','ALL',7,'elective',1),
(NULL,'ELE703','Advanced Communication','ALL',7,'elective',2),
(NULL,'ELE704','Professional Development','ALL',7,'elective',2);

---

-- SEMESTER 8

INSERT INTO courses VALUES
(NULL,'GEN801','Major Project Phase II','ALL',8,'core',6);

INSERT INTO courses VALUES
(NULL,'ELE801','Technology Policy','ALL',8,'elective',1),
(NULL,'ELE802','Global Engineering','ALL',8,'elective',1),
(NULL,'ELE803','Emerging Technologies','ALL',8,'elective',2),
(NULL,'ELE804','Innovation Strategy','ALL',8,'elective',2);

---

---

-- TEACHERS TABLE

DROP TABLE IF EXISTS teacher_courses;
DROP TABLE IF EXISTS teachers;

CREATE TABLE teachers(
teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
teacher_name TEXT,
department TEXT
);

CREATE TABLE teacher_courses(
id INTEGER PRIMARY KEY AUTOINCREMENT,
teacher_id INTEGER,
course_id INTEGER,
FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id),
FOREIGN KEY(course_id) REFERENCES courses(course_id)
);

---

---

-- TEACHERS TABLE

DROP TABLE IF EXISTS teacher_courses;
DROP TABLE IF EXISTS teachers;

CREATE TABLE teachers(
teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
teacher_name TEXT,
department TEXT
);

CREATE TABLE teacher_courses(
id INTEGER PRIMARY KEY AUTOINCREMENT,
teacher_id INTEGER,
course_id INTEGER,
FOREIGN KEY(teacher_id) REFERENCES teachers(teacher_id),
FOREIGN KEY(course_id) REFERENCES courses(course_id)
);

---

-- RULE: 1 teacher handles max 3 courses
----------------------------------------

-- CSE Teachers 
INSERT INTO teachers (teacher_name, department) VALUES
('Dr. Sharma','CSE'),('Dr. Mehta','CSE'),('Dr. Gupta','CSE'),
('Dr. Agarwal','CSE'),('Dr. Bansal','CSE'),('Dr. Khanna','CSE'),
('Dr. Arora','CSE'),('Dr. Sinha','CSE'),('Dr. Kapoor','CSE'),
('Dr. Verma','CSE'),('Dr. Jain','CSE'),('Dr. Malhotra','CSE'),
('Dr. Saxena','CSE'),('Dr. Mittal','CSE'),('Dr. Goel','CSE');

-- DSAI Teachers
INSERT INTO teachers (teacher_name, department) VALUES
('Dr. Rao','DSAI'),('Dr. Iyer','DSAI'),('Dr. Nair','DSAI'),
('Dr. Reddy','DSAI'),('Dr. Pillai','DSAI'),('Dr. Menon','DSAI'),
('Dr. Joshi','DSAI'),('Dr. Kulkarni','DSAI'),('Dr. Deshmukh','DSAI'),
('Dr. Patil','DSAI'),('Dr. Shah','DSAI'),('Dr. Bhatt','DSAI'),
('Dr. Dave','DSAI'),('Dr. Trivedi','DSAI'),('Dr. Parekh','DSAI');

-- ECE Teachers
INSERT INTO teachers (teacher_name, department) VALUES
('Dr. Singh','ECE'),('Dr. Chauhan','ECE'),('Dr. Yadav','ECE'),
('Dr. Mishra','ECE'),('Dr. Tiwari','ECE'),('Dr. Pandey','ECE'),
('Dr. Saxena','ECE'),('Dr. Tripathi','ECE'),('Dr. Srivastava','ECE'),
('Dr. Dubey','ECE'),('Dr. Goyal','ECE'),('Dr. Bhatia','ECE'),
('Dr. Suri','ECE'),('Dr. Kohli','ECE'),('Dr. Anand','ECE');

---

-- ASSIGN COURSES TO TEACHERS
-- RULE:
-- 1 teacher → max 3 courses
-- 1 course → only 1 teacher
------------------------------

-- CSE COURSES
INSERT INTO teacher_courses (teacher_id, course_id)
SELECT
(ROW_NUMBER() OVER () - 1)/3 + 1 AS teacher_id,
course_id
FROM courses
WHERE department = 'CSE';

-- DSAI COURSES
INSERT INTO teacher_courses (teacher_id, course_id)
SELECT
((ROW_NUMBER() OVER () - 1)/3 + 16) AS teacher_id,
course_id
FROM courses
WHERE department = 'DSAI';

-- ECE COURSES
INSERT INTO teacher_courses (teacher_id, course_id)
SELECT
((ROW_NUMBER() OVER () - 1)/3 + 31) AS teacher_id,
course_id
FROM courses
WHERE department = 'ECE';



-------------------------------------------------
-- INSERT SPECIFIC DSAI FACULTY
-------------------------------------------------

INSERT OR IGNORE INTO teachers (teacher_name, department) VALUES
('Dr. Shirshendu Layek','DSAI'),
('Dr. Utkarsh Mahadeo Khaire','DSAI'),
('Dr. Girish Revadigar','DSAI'),
('Dr. Animesh Chaturvedi','DSAI');

-------------------------------------------------
-- ASSIGN TEACHERS TO COURSES
-------------------------------------------------

-- DSAI401 → Dr. Shirshendu Layek
INSERT OR IGNORE INTO teacher_courses (teacher_id, course_id)
SELECT t.teacher_id, c.course_id
FROM teachers t
JOIN courses c
ON c.course_code = 'DSAI401'
WHERE t.teacher_name = 'Dr. Shirshendu Layek';

-------------------------------------------------

-- DSAI403 → Dr. Utkarsh Mahadeo Khaire
INSERT OR IGNORE INTO teacher_courses (teacher_id, course_id)
SELECT t.teacher_id, c.course_id
FROM teachers t
JOIN courses c
ON c.course_code = 'DSAI403'
WHERE t.teacher_name = 'Dr. Utkarsh Mahadeo Khaire';

-------------------------------------------------

-- DSAI404 → Dr. Girish Revadigar
INSERT OR IGNORE INTO teacher_courses (teacher_id, course_id)
SELECT t.teacher_id, c.course_id
FROM teachers t
JOIN courses c
ON c.course_code = 'DSAI404'
WHERE t.teacher_name = 'Dr. Girish Revadigar';

-------------------------------------------------

-- DSAI405 → Dr. Animesh Chaturvedi
INSERT OR IGNORE INTO teacher_courses (teacher_id, course_id)
SELECT t.teacher_id, c.course_id
FROM teachers t
JOIN courses c
ON c.course_code = 'DSAI405'
WHERE t.teacher_name = 'Dr. Animesh Chaturvedi';

---
DELETE FROM teacher_courses
WHERE id NOT IN (
    SELECT MAX(id) FROM teacher_courses GROUP BY course_id
);

---

-- ADD TEACHERS FOR ALL-DEPARTMENT COURSES (electives + GEN courses)
-- 35 unassigned ALL-dept courses → 12 teachers (max 3 courses each)

INSERT INTO teachers (teacher_name, department) VALUES
('Dr. Kaur','ALL'),
('Dr. Bose','ALL'),
('Dr. Nanda','ALL'),
('Dr. Hegde','ALL'),
('Dr. Subramaniam','ALL'),
('Dr. Varma','ALL'),
('Dr. Krishnamurthy','ALL'),
('Dr. Bhattacharya','ALL'),
('Dr. Mukherjee','ALL'),
('Dr. Choudhary','ALL'),
('Dr. Swaminathan','ALL'),
('Dr. Gopalan','ALL');

-- Assign ALL-department courses to the new teachers
-- 3 courses per teacher, ordered by semester then course_code for consistency
INSERT INTO teacher_courses (teacher_id, course_id)
SELECT
    (50 + (ROW_NUMBER() OVER (ORDER BY c.semester, c.course_code) - 1) / 3) AS teacher_id,
    c.course_id
FROM courses c
LEFT JOIN teacher_courses tc ON c.course_id = tc.course_id
WHERE tc.course_id IS NULL;


DELETE FROM teachers
WHERE teacher_id NOT IN (
    SELECT DISTINCT teacher_id FROM teacher_courses
);

---

-- EXAM COMPONENTS TABLE

CREATE TABLE exam_components (
    component_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    component_name TEXT,
    max_marks REAL,
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
);

---

-- STUDENT MARKS TABLE

CREATE TABLE student_marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_roll TEXT,
    course_id INTEGER,
    component_id INTEGER,
    marks REAL,
    FOREIGN KEY(student_roll) REFERENCES students(roll),
    FOREIGN KEY(course_id) REFERENCES courses(course_id),
    FOREIGN KEY(component_id) REFERENCES exam_components(component_id)
);

---

-- VIEW: total_marks
-- Pre-computes total marks + rank per student per subject
-- Usage: SELECT name, roll, total FROM total_marks WHERE rnk = 2;

CREATE VIEW total_marks AS
SELECT
    s.name,
    s.roll,
    c.course_name,
    c.course_code,
    SUM(sm.marks) AS total,
    DENSE_RANK() OVER (
        PARTITION BY sm.course_id
        ORDER BY SUM(sm.marks) DESC
    ) AS rnk
FROM student_marks sm
JOIN students s ON sm.student_roll = s.roll
JOIN courses c  ON sm.course_id = c.course_id
GROUP BY sm.student_roll, sm.course_id, s.name, c.course_name, c.course_code;