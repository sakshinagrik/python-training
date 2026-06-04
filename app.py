from flask import Flask,render_template

apna_nam = Flask(__name__)
stud = [
    {"name": "Tanuja", "roll": 1, "marks": 85},
    {"name": "Pratiksha", "roll": 2, "marks": 78},
    {"name": "Shlok", "roll": 3, "marks": 92},
    {"name": "Lucky", "roll": 4, "marks": 65},
]

@apna_nam.route('/')
def home():
    return render_template('Home.html',students=stud)
@apna_nam.route('/about')
def about():
    return render_template('About.html')
@apna_nam.route('/students')
def students():
    return  render_template('Student.html',students=stud)

if __name__ == '__main__':
    print("Inside main")
    apna_nam.run(debug=True)

