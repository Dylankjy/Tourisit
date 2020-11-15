from flask import Flask, render_template

app = Flask(__name__,
            static_url_path='',
            static_folder='public',
            template_folder='templates')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/id/login')
def login():
    return render_template('login.html')


@app.route('/id/signup')
def signup():
    return render_template('signup.html')


app.run(debug=True)
