# Flask imports
# Data Generation
import base64
from io import BytesIO

# Database
import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Length, NumberRange

# Authentication library
import auth as auth

#Custom class imports
from models.Listing import ListingForm, Listing

#For Images
buffered = BytesIO()
from validate_imgs import img_to_base64, validate_image

app = Flask(__name__,
            static_url_path='',
            static_folder='public',
            template_folder='templates')

#APP CONFIGS
#REMEMBER TO USE GLOBAL VARIABLE FOR THIS
app.config['SECRET_KEY'] = 'keepthissecret'
#Set file upload limit to 1MB
app.config["MAX_IMAGE_FILESIZE"] = 1 * 1024 * 1024

#CHANGE THE PASSWORD TO A GLOBAL VARIABLE
client = pymongo.MongoClient('mongodb+srv://admin:slapbass@cluster0.a6um0.mongodb.net/test')['Tourisit']

#Initialize all DBs here
shop_db = client['Listings']
user_db = client['Users']


@app.route('/testImg', methods=['GET', 'POST'])
def test_img():
    lForm = ListingForm()
    if request.method == 'POST':
        tour_img = request.files['tour_img']
        img_string = img_to_base64(tour_img)
        print(img_string)
        return render_template('tourGuides/testImg.html', form=lForm, imgBase64=img_string)
    return render_template('tourGuides/testImg.html', form=lForm, imgBase64='')


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
        return render_template('profile.html', listings=list(shop_db.find()))
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
    return render_template('customer/index-customer.html', listings=list(shop_db.find()))


# CUSTOMERS
# Marketplace: Display all listings
@app.route('/discover')
def market():
    return render_template('customer/marketplace.html', listings=list(shop_db.find()))
    # except:
    #     return 'Error trying to render'


# CUSTOMERS
# Detailed Listing: More detailed listing when listing from M clicked
@app.route('/discover/<tour_id>')
def tourListing(tour_id):
    item = shop_db.find_one({'_id': ObjectId(tour_id)})
    return render_template('customer/tourListing.html', item=item)
    # except:
    #     return f'Error for Tour_ID: {tour_id}'


# TOUR GUIDES
# Manage Listings: For Tour Guides to Edit/Manage their listings
@app.route('/listings')
def ownlisting():
    return render_template('tourGuides/ownlisting.html', listings=list(shop_db.find()))


@app.route('/listings/add', methods=['GET', 'POST'])
def makelisting():
    lForm = ListingForm()
    if request.method == 'POST':
        if lForm.validate_on_submit():
            tour_name = request.form['tour_name']
            brief_desc = request.form['tour_brief']
            detail_desc = request.form['tour_desc']
            tour_img = request.files['tour_img']
            img_string = img_to_base64(tour_img)
            tour_price = request.form['tour_price']
            print(tour_name)

            tour_listing = Listing(tour_name=tour_name, tour_brief=brief_desc, tour_desc=detail_desc,
                                   tour_price=tour_price,
                                   tour_img=img_string, tg_uid='testing')

            listingInfo = tour_listing.return_obj()
            print(listingInfo)
            shop_db.insert_one(listingInfo)
            return render_template('tourGuides/listing-success.html')
        return render_template('tourGuides/makelisting.html', form=lForm)

    else:
        return render_template('tourGuides/makelisting.html', form=lForm)


# TOUR GUIDES
# Edit Listings: When click on own listing to edit
@app.route('/listings/edit/<id>', methods=['GET', 'POST'])
def editListing(id):
    lForm = ListingForm()
    item = shop_db.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        if lForm.validate_on_submit():
            query_listing = {'_id': ObjectId(id)}
            tour_name = request.form['tour_name']
            tour_brief = request.form['tour_brief']
            tour_desc = request.form['tour_desc']
            tour_img = request.files['tour_img']
            img_string = img_to_base64(tour_img)
            tour_price = request.form['tour_price']
            updated = {
                "$set": {"tour_name": tour_name, "tour_brief": tour_brief, "tour_desc": tour_desc, "tour_img": img_string,
                         "tour_price": tour_price}}
            shop_db.update_one(query_listing, updated)

            return render_template('tourGuides/editing-success.html', id=id)
        lForm.tour_desc.default = item['tour_desc']
        lForm.process()
        return render_template('tourGuides/editListing.html', listing=item, form=lForm)

    else:
        # print(item['tour_name'])
        lForm.tour_desc.default = item['tour_desc']
        lForm.process()
        return render_template('tourGuides/editListing.html', listing=item, form=lForm)


# @app.route('/testImg', methods=['GET', 'POST'])
# def test_img():
#     lForm = ListingForm()
#     if request.method == 'POST':
#         tour_img = request.files['tour_img']
#         print(tour_img)
#     return render_template('tourGuides/testImg.html', form=lForm)


# TOUR GUIDES
# Delete Listings: When click on Delete button
@app.route('/listings/delete/<id>', methods=['GET', 'POST'])
def deleteList(id):
    listing = shop_db.delete_one({'_id': ObjectId(id)})

    return redirect('/listings')


# CUSTOMERS
# Favourites: Shows all the liked listings
@app.route('/me/favourites')
def favourites():
    return render_template('customer/favourites.html')

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
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = auth.SignupForm()
    if form.validate_on_submit():
        print("Data yes")
    else:
        print("Data no")

    if not auth.is_auth():
        return render_template('auth/signup.html', form=form)
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
