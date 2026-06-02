from flask import Flask

apna_nam = Flask(__name__)

@apna_nam.route('/')
def home():

    return '<h1>Welcome to my Flask App!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
