from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

apna_nam = Flask(__name__)

apna_nam.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coaching.db'
db = SQLAlchemy(apna_nam)

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
    batch = db.Column(db.String(50), nullable=False)
    subjects = db.Column(db.String(200), nullable=False)
    total_fee = db.Column(db.Integer, default=0)
    paid_fee = db.Column(db.Integer, default=0)
    admission_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def pending_fee(self):
        return self.total_fee - self.paid_fee

# Tujhe Junne Routes - Ashech Rahu De
@apna_nam.route('/')
def home():
    return render_template('Home.html')

@apna_nam.route('/about')
def about():
    return render_template('About.html')

@apna_nam.route('/students')
def students():
    # Ithe 'stud' list jatiye. Nanter DB varun daakhavu
    return render_template('Student.html', stud=stud)

# Navin Route - Admission Form
@apna_nam.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        new_student = Student(
            name=request.form['name'],
            phone=request.form['phone'],
            email=request.form['email'],
            batch=request.form['batch'],
            subjects=request.form['subjects'],
            total_fee=int(request.form['total_fee']),
            paid_fee=int(request.form['paid_fee'])
        )
        db.session.add(new_student)
        db.session.commit()
        return render_template('admission_success.html', name=request.form['name'])
    
    return render_template('Admission.html')

if __name__ == '__main__':
    apna_nam.run(debug=True)