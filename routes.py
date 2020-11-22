from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager

app = Flask(__name__,
            static_url_path='',
            static_folder='public',
            template_folder='templates')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'

db = SQLAlchemy(app)


# bcrypt = Bcrypt()
# login_manager = LoginManager(app)

# --------------------------------------

# Amy

# SHARED
# Support: Help desk with customer support and Apply for Pro Verified
@app.route('/support')
def support():
    try:
        return render_template('helpdesk.html')
    except:
        return 'Error trying to render'


# CUSTOMER
# Submit Review
@app.route('/review')
def review():
    try:
        return render_template('customer/review.html')
    except:
        return 'Error trying to render'


# SHARED
# User profile 
# @app.route('/users/<id>)
@app.route('/users/')
def profile():
    try:
        return render_template('profile.html')
    except:
        return 'Error trying to render'


# SHARED
# User account settings
@app.route('/me/settings')
def accountinfo():
    try:
        return render_template('setting.html')
    except:
        return 'Error trying to render'


# --------------------------------------

# ALEX

# CUSTOMERS
# Home page
@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('customer/index-customer.html')


# CUSTOMERS
# Marketplace: Display all listings
@app.route('/discover')
def market():
    try:
        return render_template('customer/marketplace.html')
    except:
        return 'Error trying to render'


# CUSTOMERS
# Detailed Listing: More detailed listing when listing from M clicked
@app.route('/discover/l/')
def tourListing():
    return render_template('customer/tourListing.html')


# CUSTOMERS
# Favourites: Shows all the liked listings
@app.route('/me/favourites')
def favourites():
    return render_template('customer/favourites.html')


# TOUR GUIDES
# Manage Listings: For Tour Guides to Edit/Manage their listings
@app.route('/listings')
def ownlisting():
    try:
        return render_template('tourGuides/ownlisting.html')
    except:
        return 'Error trying to render'


# TOUR GUIDES
# Add a Listing: For Tour Guides to add listing
@app.route('/listings/add')
def makelisting():
    try:
        return render_template('tourGuides/makelisting.html')
    except:
        return 'Error trying to render'


# --------------------------------------

# Chlorine (Cl) - 17, 35.5 [Halogen]

# CUSTOMER
# Your Bookings: Access all bookings
@app.route('/bookings')
def all_bookings():
    try:
        return render_template('customer/allBookings.html')
    except:
        return 'Error trying to render'


# CUSTOMER
# Individual Bookings
# @app.route('/bookings/<id>')
@app.route('/bookings')
def bookings():
    try:
        return render_template('customer/booking.html')
    except:
        return 'Error trying to render'


# SHARED
# Chats: Render indiv chats
@app.route('/chat')
def chat():
    try:
        return render_template('chat.html')
    except:
        return 'Error trying to render'


# TOUR GUIDES
# My Businesses: Access all gigs
@app.route('/s/businesses')
def all_businesses():
    try:
        return render_template('tourGuides/allBusinesses.html')
    except:
        return 'Error trying to render'


# TOUR GUIDES
# Individual gigs  
# @app.route('/s/businesses/<id>')
@app.route('/s/businesses')
def business():
    try:
        return render_template('tourGuides/business.html')
    except:
        return 'Error trying to render'


# --------------------------------------

# Dylan

# TOUR GUIDE
# Redirect user to dashboard if attempt to access root of /s/
@app.route('/s/')
def sellerModeDir():
    return redirect(url_for('sellerDashboard'))


# Redirect user to dashboard if attempt to access file of /s/
@app.route('/s')
def sellerModeFile():
    return redirect(url_for('sellerDashboard'))


# TOUR GUIDE
# Dashboard sex OH YES FREAK ME, DATA COME ON BABY
@app.route('/s/dashboard')
def sellerDashboard():
    return render_template('tourGuides/dashboard.html')


# INTERNAL
# Admin Dashboard -- Private internal shit
@app.route('/admin')
def adminDashboard():
    return render_template('internal/dashboard.html')


# SHARED
# Login Page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if (request.method == 'POST') and (request.form['submit_button'] == 'yes'):
        name = request.form['username']
        status = request.form['submit_button']
        return render_template('index.html')

    return render_template('auth/login.html')


# SHARED
# Sign up page
@app.route('/signup')
def signup():
    return render_template('auth/signup.html')


# Run app
app.run(debug=True)
