import uuid
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, make_response

import auth as auth

app = Flask(__name__,
            static_url_path='',
            static_folder='public',
            template_folder='templates')


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
        return render_template('profile.html', listings=Listing.query.all())
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
@app.route('/', methods=['GET'])
def home():
    return render_template('customer/index-customer.html', listings=Listing.query.all())


# CUSTOMERS
# Marketplace: Display all listings
@app.route('/discover')
def market():
    try:
        return render_template('customer/marketplace.html', listings=Listing.query.all())
    except:
        return 'Error trying to render'


# CUSTOMERS
# Detailed Listing: More detailed listing when listing from M clicked
@app.route('/discover/<int:tour_id>')
def tourListing(tour_id):
    item = Listing.query.filter_by(tour_id=tour_id).first()
    return render_template('customer/tourListing.html', item=item)
    # except:
    #     return f'Error for Tour_ID: {tour_id}'


# CUSTOMERS
# Favourites: Shows all the liked listings
@app.route('/me/favourites')
def favourites():
    return render_template('customer/favourites.html')


# TOUR GUIDES
# Manage Listings: For Tour Guides to Edit/Manage their listings
@app.route('/listings')
def ownlisting():
    return render_template('tourGuides/ownlisting.html', listings=Listing.query.all())


# TOUR GUIDES
# Delete Listings: When click on Delete button
@app.route('/listings/delete/<int:id>', methods=['GET', 'POST'])
def deleteList(id):
    listing = Listing.query.filter_by(tour_id=id).first()
    db.session.delete(listing)
    db.session.commit()

    return redirect('/listings')


# TOUR GUIDES
# Edit Listings: When click on own listing to edit
@app.route('/listings/edit/<int:id>', methods=['GET', 'POST'])
def editList(id):
    if request.method == 'POST':
        listing = Listing.query.filter_by(tour_id=id).first()

        listing.tour_name = request.form['tour-title']
        listing.tour_brief = request.form['tour-brief']
        listing.tour_desc = request.form['tour-desc']
        tour_img = request.files['tour-img'].filename
        if tour_img == '':
            tour_img = str(uuid.uuid1()) + '.jpg'
        listing.tour_img = tour_img
        listing.tour_price = request.form['tour-price']

        db.session.commit()

        return redirect(f'/discover/{id}')

    else:
        item = Listing.query.filter_by(tour_id=id).first()
        return render_template('tourGuides/editListing.html', listing=item)


# TOUR GUIDES
# Add a Listing: For Tour Guides to add listing
@app.route('/listings/add', methods=['GET', 'POST'])
def makelisting():
    if request.method == 'POST':

        # This should be the tour guide
        jake = User.query.filter_by(user_name='Jake001').first()

        tour_title = request.form['tour-title']
        brief_desc = request.form['tour-brief']
        detail_desc = request.form['tour-desc']
        tour_img = request.files['tour-img'].filename
        if tour_img == '':
            tour_img = str(uuid.uuid1()) + '.jpg'
        tour_price = request.form['tour-price']

        listing = Listing(tour_name=tour_title, tour_brief=brief_desc, tour_desc=detail_desc, tour_price=tour_price,
                          tour_img=tour_img, tour_guide=jake)

        db.session.add(listing)
        db.session.commit()
        # Replace with success msg
        return render_template('tourGuides/listing-success.html')

    else:
        return render_template('tourGuides/makelisting.html')


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
@app.route('/bookings/id')
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
@app.route('/s/businesses/id')
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


# INTERNAL
# Admin Dashboard -- Manage users
@app.route('/admin/users')
def adminUsers():
    return render_template('internal/users.html')


# INTERNAL
# Admin Dashboard -- Manage listings
@app.route('/admin/listings')
def adminListings():
    return render_template('internal/listings.html')


# SHARED
# Login Page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if not auth.is_auth():
        if (request.method == 'POST') and (request.form['submit_button'] == 'yes'):
            name = request.form['username']
            status = request.form['submit_button']
        return render_template('auth/login.html')
    else:
        return redirect(url_for('home'))


# SHARED
# Sign up page
@app.route('/signup')
def signup():
    if not auth.is_auth():
        return render_template('auth/signup.html')
    else:
        return redirect(url_for('home'))
    # return render_template('auth/signup.html')


# Run app
if __name__ == '__main__':
    app.run(debug=True)

# This edits the tour_name of the 4th listing
# listing = Listing.query.filter_by(tour_id=4).first()
# listing.tour_name = 'New nreame'
# db.session.commit()


# Get the last listing (The most recent one)
# print(Listing.query.all()[-1])


# class User():
#     __tablename__ = 'users'
#     user_id = db.Column(db.Integer, primary_key=True, unique=True)
#     user_name = db.Column(db.String(30), nullable=False, unique=True)
#     user_password = db.Column(db.String(30), nullable=False)
#     user_rating = db.Column(db.String(30), nullable=False)
#     user_img = db.Column(db.String(30))
#
#
# class Customer(db.Model, User):
#     __tablename__ = 'cutomers'
#     wishlist = db.Column(db.String(30), nullable=False, unique=True)
#
#
# class TourGuides(db.Model, User):
#     __tablename__ = 'tourguides'
#     #Creates an artificial column in 'Listing' table called 'tour_guide'.
#     # TourGuides['tours'] = Listing
#     # Listing['tour_guide'] = TourGuides
#     tours = db.relationship('Listing', backref='tour_guide')
#
#
# class Listing(db.Model):
#     __tablename__ = 'listings'
#     tour_id = db.Column(db.Integer, primary_key=True)
#     tour_name = db.Column(db.String(30), nullable=False, unique=True)
#     tour_brief = db.Column(db.String(50), nullable=False)
#     tour_desc = db.Column(db.String(300), nullable=False)
#     tour_price = db.Column(db.Integer, nullable=False)
#     tour_img = db.Column(db.String(10), unique=True)
#     date_created = db.Column(db.DateTime, default=datetime.now)
