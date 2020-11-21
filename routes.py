from flask import Flask, render_template, request, redirect, url_for
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

app = Flask(__name__,
            static_url_path='',
            static_folder='public',
            template_folder='templates')

# bcrypt = Bcrypt()
# login_manager = LoginManager(app)


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if (request.method == 'POST') and (request.form['submit_button'] == 'yes'):
        name = request.form['username']
        status = request.form['submit_button']
        return render_template('index.html')

    info = {}
    return render_template('login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/s/')
def sellerMode():
    return redirect("/s/dashboard", code = 302)

@app.route('/s/dashboard')
def sellerDashboard():
    return render_template('dashboard.html')


@app.route('/market')
def market():
    try:
        return render_template('market.html')
    except:
        return 'Error trying to render'


@app.route('/makelisting')
def makelisting():
    try:
        return render_template('makelisting.html')
    except:
        return 'Error trying to render'


@app.route('/ownlisting')
def ownlisting():
    try:
        return render_template('ownlisting.html')
    except:
        return 'Error trying to render'


@app.route('/bookings')
def bookings():
    try:
        return render_template('bookings.html')
    except:
        return 'Error trying to render'


@app.route('/review')
def review():
    try:
        return render_template('review.html')
    except:
        return 'Error trying to render'


@app.route('/tourListing')
def tourListing():
    return render_template('tourListing.html')

@app.route('/helpdesk')
def helpdesk():
    try:
        return render_template('helpdesk.html')
    except:
        return 'Error trying to render'

app.run(debug=True)
