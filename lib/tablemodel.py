import os
import sqlite3

class DatabaseModel:
    """This class is a wrapper around the sqlite3 database. It provides a simple interface that maps methods
    to database queries. The only required parameter is the database file."""

    def __init__(self, database_file):
        self.database_file = database_file
        if not os.path.exists(self.database_file):
            raise FileNotFoundError(f"Could not find database file: {database_file}")
        
    # Using the built-in sqlite3 system table, return a list of all tables in the database
    def get_table_list(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        return tables


### Student functions
    # Checks if the entered student number and password combination is valid and returns the student's info if so.
    def validate_login(self, student_number, password):
        cursor = sqlite3.connect(self.database_file).cursor()
        if len(student_number) == 7:
            cursor.execute(f"SELECT * FROM student WHERE student_number = '{student_number}'")
            account = cursor.fetchone()
            cursor.close()
            if account == None or password != account[4]:
                return False
        else:
            cursor.execute(f"SELECT * FROM teacher WHERE teacher_id = '{student_number}'")
            account = cursor.fetchone()
            cursor.close()
            if account == None or password != account[3]:
                return False
        return account

    # -----------

    # Creates a new student with the entered information.
    def create_student(self, first_name, last_name, password):
        student_number = self.create_student_number()
        db = sqlite3.connect(self.database_file)
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO student (student_number, first_name, last_name, password) VALUES ('{student_number}', '{first_name}', '{last_name}', '{password}')")
        db.commit()
        db.close()

    def get_table_content(self, table_name):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 40")
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()
                
        return table_content, table_headers
    # -----------

    def get_student_by_id(self, id):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM student WHERE id = '{id}'")
        data = cursor.fetchone()
        return data

    def create_student_number(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT (MAX(id) + 1) FROM student")
        new_id = cursor.fetchone()
        if new_id[0] == None:
            number = "1"
        else:
            number = str(new_id[0])
        cursor.close()

        while len(number) < 7:
            number = "0" + number
        return number

    # -----------

    # Updates a user.
    def update_student(self, id, first_name, last_name, password):
        db = sqlite3.connect(self.database_file)
        cursor = db.cursor()
        qry = f"UPDATE student SET first_name = '{first_name}', last_name = '{last_name}', password = '{password}' WHERE id = '{id}'"
        cursor.execute(qry)
        db.commit()
        db.close()

    # -----------

    # Deletes a user.
    def delete_student(self, id):
        db = sqlite3.connect(self.database_file)
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM student WHERE id = '{id}'")
        db.commit()
        db.close()

    # Returns a user's password, based on a given id. 
    def get_password_by_id(self, id, table):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT password FROM {table} WHERE id = '{id}'")
        pwd = cursor.fetchone()
        cursor.close()
        return pwd[0]

###

### Teacher functions

    def create_teacher(self, first_name, last_name, password, isAdmin=1):
        db = sqlite3.connect(self.database_file)
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO teacher (first_name, last_name, password, isAdmin) VALUES ('{first_name}', '{last_name}', '{password}', '{isAdmin}')")
        db.commit()
        db.close()

    def update_teacher(self, id, first_name, last_name, password):
        db = sqlite3.connect(self.database_file)
        cursor = db.cursor()
        qry = f"UPDATE teacher SET first_name = '{first_name}', last_name = '{last_name}', password = '{password}' WHERE id = '{id}'"
        cursor.execute(qry)
        db.commit()
        db.close()

    def delete_teacher(self, id):
        db = sqlite3.connect(self.database_file)
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM teacher WHERE teacher_id = '{id}'")
        db.commit()
        db.close()

    def get_teacher_by_id(self, id):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM teacher WHERE teacher_id = '{id}'")
        data = cursor.fetchone()
        return data
###

### Admin Interface

    def get_students(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM student")
        data = cursor.fetchall()
        columns = [column_name[0] for column_name in cursor.description]
        return data, columns
    
    def get_teachers(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM teacher")
        data = cursor.fetchall()
        columns = [column_name[0] for column_name in cursor.description]
        return data, columns
    
    def get_student_in_meeting(self, meeting_id):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT student.* FROM student JOIN meeting_assignment ON student.id = meeting_assignment.student_id WHERE meeting_assignment.meeting_id = '{meeting_id}'")
        data = cursor.fetchall()
        return data
    
    def get_presence_db(self, meeting_id, student_id):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT present FROM attendance WHERE meeting_id = '{meeting_id}' AND student_number = '{student_id}'")
        data = cursor.fetchall()
        return data
    
    
    def get_course_name(self, meeting_id):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT courses.course_name FROM meeting JOIN courses ON meeting.course_id = courses.course_id WHERE meeting.meeting_id = '{meeting_id}'")
        data = cursor.fetchall()
        return data
    
    def get_class_by_id(self, id):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM class WHERE id = '{id}'")
        data = cursor.fetchone()
        return data
    
    def update_attendance(self, student_number, meeting_id, presence):
        db = sqlite3.connect(self.database_file)
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO attendance (student_number, meeting_id, present) VALUES (?, ?, ?)", (student_number, meeting_id, presence))
        db.commit()
        db.close()
    

    # Gets all content from a table.
    def get_content(self, table_name):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        columns = [column_name[0] for column_name in cursor.description]
        return data, columns

    def get_meetings(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM meeting")
        data = cursor.fetchall()
        columns = [column_name[0] for column_name in cursor.description]
        return data, columns

    def get_meeting(self, course_id):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM meeting WHERE course_id == '{course_id}'")
        data = cursor.fetchall()
        columns = [column_name[0] for column_name in cursor.description]
        return data, columns
    
    def get_course_by_name(self, name):
        print(name)
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM courses WHERE course_name = '{name}'")
        id = cursor.fetchone()
        print(id)
        return id