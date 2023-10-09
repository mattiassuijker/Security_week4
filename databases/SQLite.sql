--SQLite
-- CREATE TABLE student (
-- 	id INTEGER PRIMARY KEY,
-- 	student_number varchar(7) NOT NULL,
-- 	first_name varchar(50) NOT NULL,
-- 	last_name varchar(50) NOT NULL,
-- 	password varchar(100) NOT NULL,
-- 	CONSTRAINT student_number_unique UNIQUE (student_number)
-- );

-- DROP TABLE student;

-- CREATE TABLE class (
-- 	id INTEGER PRIMARY KEY,
-- 	class_shorthand varchar(10) NOT NULL,
-- 	class_name varchar(50) NOT NULL,
-- 	CONSTRAINT class_shorthand_unique UNIQUE (class_shorthand),
-- 	CONSTRAINT class_name_unique UNIQUE (class_name)
-- );

-- CREATE TABLE class_assignment (
-- 	id INTEGER PRIMARY KEY,
-- 	class_id INTEGER NOT NULL,
-- 	student_id INTEGER NOT NULL,
-- 	FOREIGN KEY(class_id) REFERENCES class(id),
-- 	FOREIGN KEY(student_id) REFERENCES student(id)
-- );

-- INSERT INTO class(class_shorthand, class_name) VALUES ('SWDVT1C', 'Software Development Voltijd');
-- INSERT INTO class(class_shorthand, class_name) VALUES ('INF1A', 'Informatica');

-- INSERT INTO class_assignment(class_id, student_id) VALUES (1, 1);

-- SELECT s.first_name, s.last_name, c.class_shorthand FROM class_assignment ca JOIN student s ON ca.student_id = s.id JOIN class c ON c.id = ca.class_id;

-- CREATE TABLE meeting (
-- 	meeting_id INTEGER PRIMARY KEY,
-- 	course_id INTEGER NOT NULL,
-- 	date DATE NOT NULL,
-- 	start_time INTEGER NOT NULL,
-- 	end_time INTEGER NOT NULL,
-- 	FOREIGN KEY(course_id) REFERENCES course(course_id)
-- );

-- CREATE TABLE meeting_assignment (
-- 	meeting_assignment_id INTEGER PRIMARY KEY,
-- 	meeting_id INTEGER NOT NULL,
-- 	student_id INTEGER NOT NULL,
-- 	teacher_id INTEGER NOT NULL,
-- 	FOREIGN KEY(meeting_id) REFERENCES meeting(meeting_id),
-- 	FOREIGN KEY(student_id) REFERENCES student(id),
-- 	FOREIGN KEY(teacher_id) REFERENCES teacher(teacher_id)
-- );

-- CREATE TABLE teacher (
-- 	teacher_id INTEGER PRIMARY KEY,
-- 	first_name	VARCHAR(50) NOT NULL,
-- 	last_name	VARCHAR(50) NOT NULL,
-- 	password	VARCHAR(50) NOT NULL,
-- 	isAdmin BOOLEAN DEFAULT 0 CHECK (isAdmin IN (0, 1))
-- );

-- CREATE TABLE courses (
-- 	course_id INTEGER PRIMARY KEY,
-- 	course_code VARCHAR(10),
-- 	course_name VARCHAR(50)
-- );

-- INSERT INTO courses(course_code, course_name) VALUES ('ADNED01VX', 'Nederlands');

-- INSERT INTO meeting(course_id, date, start_time, end_time) VALUES (5, '27-04-2023', 1400, 1700);



-- CREATE TABLE attendance (
-- 	meeting_id INTEGER NOT NULL,
-- 	student_id INTEGER NOT NULL,
--  present BOOLEAN DEFAULT 0 CHECK (present IN (0, 1)), 
--  FOREIGN KEY(meeting_id) REFERENCES meeting(meeting_id),
--  FOREIGN KEY(student_id) REFERENCES student(id)
--  );


-- INSERT INTO attendance (meeting_id, student_id) VALUES (3, 1);

-- UPDATE courses SET course_name = 'Werkplaats' WHERE course_id = 1;