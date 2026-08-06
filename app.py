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
    subjects = db.Column(db.String(200), nullable=False)
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
# Tujhe Junne Routes - Ashech Rahu De
@app.route('/')
def home():
    return render_template('Home.html')

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
    return render_template("dashboard.html")
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
    search = request.args.get("search")

    if search:
       students = Student.query.filter(Student.name.contains(search) ).all()
    else:
       students = Student.query.all()

    return render_template( "student_list.html",students=students,search=search)

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
        photo = request.files['photo']

        filename = secure_filename(photo.filename)

        photo.save(os.path.join("static/uploads", filename))
        new_student = Student(

            name=request.form['name'],
            phone=request.form['phone'],
            photo=filename,
            email=request.form['email'],
            batch=request.form['batch'],
            subjects=request.form['subjects'],
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
        student.subjects = request.form['subjects']
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
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        flash("✅ Login Successful!", "success")
        session['user']="test"
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        flash("✅ Registration Successful!", "success")
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