from flask import Flask

app = Flask(__name__)
@app.route('/')
def home():
    return '''
    <h1>Coaching Class Manager</h1>
    <h2>Welcome to Parhad Classes</h2>
    <p>This project manages coaching class student records.</p>

    <h3>Available Pages</h3>
    <p>/records - Student Records</p>
    <p>/teacher - Teacher Information</p>
    '''
@app.route('/records')
def records():
    return '''
    <h1>Student Records</h1>
    <p>Rahul - Python</p>
    <p>Sham - Java</p>
    <p>Shashank - C++</p>
    '''


@app.route('/teacher')
def teacher():
    return '''
    <h1>Teacher Information</h1>
    <p>Teacher Name: Parhad Sir</p>
    <p>Subject: Python</p>
    <p>Experience: 10 Years</p>
    '''

if __name__ == '__main__':
    app.run(debug=True)