from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__,
            static_url_path='',
            static_folder='public',
            template_folder='templates')


@app.route('/', methods=['POST', 'GET'])
def home():
    info = {}
    return render_template('index.html', info=info)


@app.route('/login', methods=['POST', 'GET'])
def login():
    global info
    if (request.method == 'POST') and (request.form['submit_button'] == 'yes'):
        name = request.form['username']
        status = request.form['submit_button']
        info = {'name': name, 'status': status}
        return render_template('index.html', info=info)

    info = {}
    return render_template('login.html', info=info)


@app.route('/signup')
def signup():
    return render_template('signup.html')


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


@app.route('/tourListing')
def tourListing():
    return render_template('tourListing.html')


app.run(debug=True)
