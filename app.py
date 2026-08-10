from flask import Flask, render_template, request,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'sakshi123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coaching.db'
db = SQLAlchemy(app)

# Tujhi juni list - Student.html sathi
stud = [
    {'id': 1, 'name': 'Sakshi', 'batch': 'JEE 2026', 'pending_fee': 5000},
    {'id': 2, 'name': 'Shlok', 'batch': 'NEET 2026', 'pending_fee': 0}
]

# Navin Database Table - Admission sathi
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100))
    photo = db.Column(db.String(100))
    batch = db.Column(db.String(50), nullable=False)
    total_fee = db.Column(db.Integer, default=0)
    paid_fee = db.Column(db.Integer, default=0)
    admission_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def pending_fee(self):
        return self.total_fee - self.paid_fee
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
class ClassSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    subject = db.Column(db.String(100), nullable=False)
    teacher = db.Column(db.String(100), nullable=False)

    class_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.String(20), nullable=False)
    end_time = db.Column(db.String(20), nullable=False)

    mode = db.Column(db.String(20), nullable=False)  # Online / Offline

    room = db.Column(db.String(100))
    meeting_link = db.Column(db.String(500))

    topic = db.Column(db.String(200))
    batch = db.Column(db.String(100))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
# Tujhe Junne Routes - Ashech Rahu De
@app.route('/')
def home():
    return render_template("Home.html")
@app.route('/about')
def about():
    return render_template('About.html')
@app.route('/ai')
def ai_assistant():
    return render_template("ai_assistant.html")
@app.route("/career_guide")
def career_guide():
    return "<h2>Career Guide AI Page</h2>"
@app.route("/doubt_solver")
def doubt_solver():
    return render_template("doubt_solver.html")
@app.route("/motivation_corner")
def motivation_corner():
    return render_template("motivation_corner.html")
@app.route("/quiz_generator")
def quiz_generator():
    return "<h2>Daily Quiz Generator Page</h2>"

@app.route('/coaching_quiz')
def coaching_quiz():
    return render_template("coaching_quiz.html")
@app.route("/study_plan")
def study_plan():
    return render_template("study_plan.html")
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please Login First", "warning")
        return redirect(url_for('login'))

    students = Student.query.all()

    total_students = len(students)

    paid_students = 0
    pending_students = 0
    pending_fees = 0

    total_fee = 0
    paid_fee = 0

    for student in students:

        student_total_fee = student.total_fee or 0
        student_paid_fee = student.paid_fee or 0

        total_fee += student_total_fee
        paid_fee += student_paid_fee

        if student.pending_fee <= 0:
            paid_students += 1
        else:
            pending_students += 1
            pending_fees += student.pending_fee

    if total_fee > 0:
        fee_progress = round((paid_fee / total_fee) * 100)
    else:
        fee_progress = 0

    recent_admissions = Student.query.order_by(
        Student.admission_date.desc()
    ).limit(3).all()

    new_admissions = total_students

    return render_template(
        "dashboard.html",
        total_students=total_students,
        paid_students=paid_students,
        pending_students=pending_students,
        pending_fees=pending_fees,
        fee_progress=fee_progress,
        new_admissions=new_admissions,
        recent_admissions=recent_admissions,
        paid_fee=paid_fee,
        total_fee=total_fee
    )
@app.route('/learning_hub')
def learning_hub():

    if "user" not in session:
        flash("Please Login First", "warning")
        return redirect(url_for('login'))

    return render_template("learning_hub.html")
@app.route('/class_schedule')
def class_schedule():

    if "user" not in session:
        flash("Please Login First", "warning")
        return redirect(url_for('login'))

    schedules = ClassSchedule.query.order_by(
        ClassSchedule.class_date.asc(),
        ClassSchedule.start_time.asc()
    ).all()

    return render_template(
        'class_schedule.html',
        schedules=schedules
    )
@app.route('/admin/add_class_schedule', methods=['GET', 'POST'])
def add_class_schedule():

    if "user" not in session:
        flash("Please Login First", "warning")
        return redirect(url_for('login'))

    if session.get("role") != "admin":
        flash("Admin access required.", "danger")
        return redirect(url_for('class_schedule'))

    if request.method == 'POST':

        schedule = ClassSchedule(
            subject=request.form['subject'],
            teacher=request.form['teacher'],
            class_date=datetime.strptime(
                request.form['class_date'],
                '%Y-%m-%d'
            ).date(),
            start_time=request.form['start_time'],
            end_time=request.form['end_time'],
            mode=request.form['mode'],
            room=request.form.get('room', ''),
            meeting_link=request.form.get('meeting_link', ''),
            topic=request.form.get('topic', ''),
            batch=request.form.get('batch', '')
        )

        db.session.add(schedule)
        db.session.commit()

        flash("✅ Class schedule created successfully!", "success")

        return redirect(url_for('class_schedule'))

    return render_template('add_class_schedule.html')
@app.route('/admin/edit_class_schedule/<int:id>', methods=['GET', 'POST'])
def edit_class_schedule(id):

    if "user" not in session:
        flash("Please Login First", "warning")
        return redirect(url_for('login'))

    if session.get("role") != "admin":
        flash("Admin access required.", "danger")
        return redirect(url_for('class_schedule'))

    schedule = ClassSchedule.query.get_or_404(id)

    if request.method == 'POST':

        schedule.subject = request.form['subject']
        schedule.teacher = request.form['teacher']

        schedule.class_date = datetime.strptime(
            request.form['class_date'],
            '%Y-%m-%d'
        ).date()

        schedule.start_time = request.form['start_time']
        schedule.end_time = request.form['end_time']

        schedule.mode = request.form['mode']

        schedule.room = request.form.get('room', '')
        schedule.meeting_link = request.form.get('meeting_link', '')

        schedule.topic = request.form.get('topic', '')
        schedule.batch = request.form.get('batch', '')

        db.session.commit()

        flash("✅ Class schedule updated successfully!", "success")

        return redirect(url_for('class_schedule'))

    return render_template(
        'add_class_schedule.html',
        schedule=schedule
    )
@app.route('/admin/delete_class_schedule/<int:id>')
def delete_class_schedule(id):

    if "user" not in session:
        flash("Please Login First", "warning")
        return redirect(url_for('login'))

    if session.get("role") != "admin":
        flash("Admin access required.", "danger")
        return redirect(url_for('class_schedule'))

    schedule = ClassSchedule.query.get_or_404(id)

    db.session.delete(schedule)
    db.session.commit()

    flash("✅ Class schedule deleted successfully!", "success")

    return redirect(url_for('class_schedule'))
@app.route('/live_courses')
def live_courses():

    if "user" not in session:
        flash("Please Login First", "warning")
        return redirect(url_for('login'))

    live_classes = ClassSchedule.query.filter_by(
        mode="Online"
    ).order_by(
        ClassSchedule.class_date.asc(),
        ClassSchedule.start_time.asc()
    ).all()

    return render_template(
        "live_course.html",
        live_classes=live_classes
    )
@app.route('/video_courses')
def video_courses():

    if "user" not in session:
        flash("Please Login First", "warning")
        return redirect(url_for('login'))

    return render_template("video_course.html")
@app.route('/combo_courses')
def combo_courses():
    return render_template('combo_courses.html')
@app.route('/demo_courses')
def demo_courses():
    return render_template('demo_courses.html')
@app.route('/demo_course')
def demo_course():

    exam = request.args.get('exam')

    if not exam:
        exam = "MHT-CET"

    return render_template(
        'demo_course.html',
        exam=exam
    )
@app.route('/class_notes')
def class_notes():
    return render_template('class_notes.html')
@app.route('/syllabus')
def syllabus():
    return render_template('syllabus.html')
@app.route('/class-tests')
def class_tests():
    return render_template('class_tests.html')
@app.route('/performance')
def performance():
    return render_template('performance.html')
@app.route('/progress')
def progress():
    return render_template('progress.html')
@app.route('/achievements')
def achievements():
    return render_template('achievements.html')
@app.route('/students')
def students():
    return render_template('Student.html', stud=stud)
# Navin Route - Admission Form
@app.route('/student_list')
def student_list():

    print(session)

    if "user" not in session:
        flash("Please Login First", "warning")
        return redirect(url_for('login'))

    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    if search:
        students = Student.query.filter(
            Student.name.contains(search)
        ).paginate(
            page=page,
            per_page=5,
            error_out=False
        )
    else:
        students = Student.query.paginate(
            page=page,
            per_page=5,
            error_out=False
        )

    return render_template(
        "student_list.html",
        students=students,
        search=search
    )
@app.route('/search_students')
def search_students():

    if "user" not in session:
        return jsonify([])

    search = request.args.get("search", "")

    if search:
        students = Student.query.filter(
            Student.name.ilike(f"%{search}%")
        ).all()
    else:
        students = Student.query.all()

    data = []

    for s in students:
        data.append({
            "id": s.id,
            "name": s.name,
            "phone": s.phone,
            "email": s.email,
            "batch": s.batch,
            "subjects": s.subjects,
            "total_fee": s.total_fee,
            "paid_fee": s.paid_fee
        })

    return jsonify(data)


@app.route('/admission', methods=['GET', 'POST'])
def admission():

    print(dict(session))

    if "user" not in session:
        flash("Please Login First", "warning")
        return redirect(url_for('login'))

    if request.method == 'POST':

        # Photo is OPTIONAL
        photo = request.files.get('photo')

        filename = ""

        if photo and photo.filename:
            filename = secure_filename(photo.filename)
            photo.save(os.path.join("static/uploads", filename))

        new_student = Student(
            name=request.form['name'],
            phone=request.form['phone'],
            photo=filename,
            email=request.form['email'],
            batch=request.form['batch'],
            total_fee=int(request.form['total_fee'] or 0),
            paid_fee=int(request.form['paid_fee'] or 0)
        )

        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for('student_list'))

    return render_template("Admission.html")
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)

    if request.method == 'POST':
        student.name = request.form['name']
        student.phone = request.form['phone']
        student.email = request.form['email']
        student.batch = request.form['batch']
        student.total_fee = int(request.form['total_fee'] or 0)
        student.paid_fee = int(request.form['paid_fee'] or 0)

        db.session.commit()

        return redirect(url_for('student_list'))

    return render_template("Admission.html", student=student)
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/student_list')
ADMIN_USERS = {
    "sakshinagrik": "sakshi@4321",
    "Anuradhakarhale": "anu@4321"
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        print("LOGIN:", repr(username), repr(password))

        if username in ADMIN_USERS and ADMIN_USERS[username] == password:
            session['user'] = username
            session['role'] = 'admin'

            flash("✅ Admin Login Successful!", "success")
            return redirect(url_for('dashboard'))

        flash("❌ Invalid username or password!", "danger")
        return redirect(url_for('login'))

    return render_template('login.html')
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        session['user'] = username
        session['role'] = 'user'

        flash("✅ Registration Successful! Please Login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')
   
@app.route('/logout')
def logout():
    session.clear()
    flash("Logout Successful!", "success")
    return redirect(url_for('login'))
print(app.url_map)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)