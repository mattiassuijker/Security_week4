import os.path
import sys
import datetime
import qrcode

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from functools import wraps

from lib.tablemodel import DatabaseModel

LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
# This command creates the "<application directory>/databases/dummydata.db" path
DATABASE_FILE = os.path.join(app.root_path, 'databases', 'dummydata.db')
dbm = DatabaseModel(DATABASE_FILE)

# A secret key is needed to allow for sessions.
app.secret_key = 'Code wizards'


# A decorator to check if you are logged in. If you are, it redirects you to the requested page.
#   If you are not logged in, it instead redirects you to the login page.
#
# Used sources:
# https://stackoverflow.com/questions/35307676/check-login-status-flask
# https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/?highlight=wrap
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'loggedin' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap

# A decorator to check if you are using an administrator account. If you are, it redirects you to the requested page.
#   If you are not using an administrator account, it instead redirects you to the home page.
#
# Used sources:
# https://stackoverflow.com/questions/35307676/check-login-status-flask
# https://flask.palletsprojects.com/en/2.0.x/patterns/viewdecorators/?highlight=wrap
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'isAdmin' in session and session['isAdmin'] == 1:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return wrap

# When requesting a new page, checks to see if the session lifetime has expired.
#   If so, it will clear the session data and you will be required to login again.
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(days=1000)
    session.modified = True
    
# The home page. You are directed here upon establishing a connection to the website.
@app.route("/")
@login_required
def index():
    return render_template(
        "home.html"
    )

@app.route("/checkin")
@login_required
def create_qrcode():
    # Generate a QR code with the class information
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data("")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("static/images/qr_code.png")
    print(img)
    # Return a template with the QR code
    return render_template("checkin.html", img=img)

@app.route("/attendees")
@login_required
def get_table_students(table_name=None):
    rows_students = dbm.get_table_content(table_name = 'student')
    return render_template("attendees.html", students=rows_students[0])

# The login page. When given a student number and password pair, checks to see if the credentials are valid. 
#   If so, logs the user in, creates session data for the user and redirects to the question page. 
#   If not, displays an error on the screen.
# Website used: https://codeshack.io/login-system-python-flask-mysql/
@app.route("/login", methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST' and 'user_number' in request.form and 'password' in request.form:
        user_number = request.form['user_number']
        password = request.form['password']
        account = dbm.validate_login(user_number, password)
        if(account):
            session['loggedin'] = True
            session['id'] = account[0]
            session['user_number'] = account[1]
            if(len(account[1])!=7):
                session['isAdmin'] = account[4]
            return redirect(url_for('index'))
        else:
            error = "Ongeldig student nummer en/of wachtwoord. Probeer het opnieuw."
    return render_template(
        "login.html", 
        error = error
    )

# Logs the user out by removing the session data. The redirects the user to the home page.
# Website used: https://codeshack.io/login-system-python-flask-mysql/
@app.route("/logout")
@login_required
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('user_number', None)
    if('isAdmin' in session):
        session.pop('isAdmin', None)
    return render_template(
        "login.html"
    )

@app.route("/overview", methods= ['GET'])
@login_required
def overview():
    if request.method == 'GET':
        data, columns = dbm.get_meetings()
    return render_template(
        "overview-table.html", 
        data = data,
        columns = columns
    )

@app.route("/overview/<course>", methods = ["GET", "POST"])
def overview_select(course):
    id = dbm.get_course_by_name(course) 
    data, columns = dbm.get_meeting(id[0])
    return render_template(
        "overview-table.html",
        data = data,
        columns = columns,
        course = course
    )



@app.route('/getmeeting', methods= ['GET'])
@login_required
def get_meeting(course_id = 1):
    if request.method == "GET":
        if (request.args.get('current_course') != None):
            course_id = request.args.get('current_course')
        data, columns = dbm.get_meeting(course_id)
    return render_template(
        "overview-table.html",
        data = data,
        columns = columns
    )

@app.route("/schedule")
@login_required
def schedule():
    return render_template(
        "schedule.html"
    )

@app.route("/admin")
@admin_required
def admin():
    if request.method == "GET":
        if (request.args.get('current_table') != None):
            table = request.args.get('current_table')
        else:
            table = 'teacher'
        data, columns = dbm.get_content(table)
    return render_template(
        "admin.html",
        data = data,
        columns = columns,
        table = table
    )

@app.route("/admin/<table>", methods = ["GET", "POST"])
@admin_required
def admin_select(table):
    data, columns = dbm.get_content(table)
    return render_template(
        "admin.html",
        data = data,
        columns = columns,
        table = table
    )

@app.route('/getitem')
@login_required
def getitem():
    if(request.args.get('table') == 'teacher'):
        data = dbm.get_teacher_by_id(request.args.get('id'))
        return jsonify(data)
    elif(request.args.get('table') == 'student'):
        data = dbm.get_student_by_id(request.args.get('id'))
        return jsonify(data)
    elif(request.args.get('table') == 'class'):
        data = dbm.get_class_by_id(request.args.get('id'))
        return jsonify(data)
    else:
        return redirect('admin.html', code=404)

@app.route("/present")
#@login_required
def present():
    return render_template(
        "present.html"
    )

    
@app.route('/students')
@login_required
def get_students():
    students = dbm.get_table_content(table_name = 'student')
    student_list = []
    for student in students[0]:
        student_dict = {'id': student[0], 'student_number': student[1], 'first_name': student[2]}
        student_list.append(student_dict)
    return jsonify(student_list)

# @app.route('/groups')
# @login_required
# def get_groups():
#     groups = dbm.get_table_content(table_name = 'class')
#     group_list = []
#     for group in groups[0]:
#         group_dict = {'id': group[0], 'class_shorthand': group[1]}
#         group_list.append(group_dict)
#     return jsonify(group_list)

# @app.route('/groups_class/<class_id>')
# def get_student(class_id):
#     students = dbm.get_student_in_class(class_id = class_id)
#     student_list = []
#     for student in students:
#         student_dict = {'id': student[0], 'student_number': student[1], 'first_name': student[2],'last_name': student[3]}
#         student_list.append(student_dict)
#     return jsonify(student_list)
@app.route('/groups/<meeting_id>')
def get_student(meeting_id):
    students = dbm.get_student_in_meeting(meeting_id = meeting_id)
    student_list = []
    for student in students:
        student_dict = {'id': student[0], 'student_number': student[1], 'first_name': student[2],'last_name': student[3]}
        student_list.append(student_dict)
    return jsonify(student_list)

@app.route('/set_student_present', methods=['POST'])
def set_student_present():
    student_number = request.form.get('student_number')
    meeting_id = request.form.get('meeting_id')
    presence = True
    dbm.update_attendance(student_number, meeting_id, presence)
    # code to mark student as present in database using student_id
    return redirect("/")

# @app.route('/groups/<meeting_id>')
# def get_groups(meeting_id):
#     class_id = dbm.get_class_id(meeting_id = meeting_id)
#     return jsonify(class_id[0])


@app.route('/course/<meeting_id>')
def get_course_name(meeting_id):
    course_name = dbm.get_course_name(meeting_id = meeting_id)

    return jsonify(course_name[0])

@app.route('/is_present/<meeting_id>/<student_id>')
def get_presence(meeting_id, student_id):
    presence = dbm.get_presence_db(meeting_id = meeting_id, student_id = student_id)
    print('hello world')
    return jsonify(presence[0])

@app.route("/admin_data", methods=["GET", "POST"])
def admin_data(table = 'teacher'):
    if request.method == 'GET':
        if table == 'teacher':
            data, columns = dbm.get_teachers()
        elif table == 'class':
            data, columns = dbm.get_class()
        elif table == 'student':
            data, columns = dbm.get_students()

        return render_template(
            "admin.html",
            data = data,
            columns = columns,
            current_table = table
        )

# Creates a new student using the information provided in the completed form.
@app.route("/createstudent", methods=['GET', 'POST'])
#@login_required
def create_student():
    dbm.create_student(request.form.get('first_name'), request.form.get('last_name'), request.form.get('password'))
    if request.method == 'POST':
        return redirect("/", code=302) 
    
# Creates a new student using the information provided in the completed form.
@app.route("/createteacher", methods=['GET', 'POST'])
#@login_required
def create_teacher():
    dbm.create_teacher(request.form.get('first_name'), request.form.get('last_name'), request.form.get('password'))
    if request.method == 'POST':
        return redirect("/", code=302) 

@app.route("/edituser", methods=['POST'])
def edit_user():
    if(request.form.get('update-table') == 'teacher'):
        dbm.update_teacher(request.form.get('id'), request.form.get('first_name'), request.form.get('last_name'), request.form.get('password'))
        if request.method == 'POST':
            return redirect('/admin/teacher?', code=302)
    elif(request.form.get('update-table') == 'student'):
        dbm.update_student(request.form.get('id'), request.form.get('first_name'), request.form.get('last_name'), request.form.get('password'))
        if request.method == 'POST':
            return redirect('/admin/student?', code=302)
    elif(request.form.get('update-table') == 'class'):
        pass
    else:
        return redirect('/admin', code=404)
    
# Deletes a specific user using their id.
@app.route("/deleteuser", methods=['GET', 'POST'])
@admin_required
def delete_user():
    if(request.form.get('delete-table') == 'teacher'):
        dbm.delete_teacher(request.form.get('id'))
        if request.method == 'POST':
            return redirect('/admin/teacher?', code=302)
    elif(request.form.get('delete-table') == 'student'):
        dbm.delete_student(request.form.get('id'))
        if request.method == 'POST':
            return redirect('/admin/student?', code=302)
    elif(request.form.get('delete-table') == 'class'):
        pass
    else:
        return redirect('/admin', code=404)
  

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)