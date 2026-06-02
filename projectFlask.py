from flask import Flask
 
Coaching = Flask(__name__)
@Coaching.route('/')
def parhad():
    return '<h1>Welcome to parahad classess</h1>'
@Coaching.route('/Teaching Staff')
def staff():
    return '<h1>Our teaching staff is very good</h1>'
@Coaching.route('/Students')
def students():
    return '<h1>Our students are very good</h1>'
if __name__ == '__main__':
    Coaching.run(debug=True)


