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
from models.model import Listing

buffered = BytesIO()

app = Flask(__name__,
            static_url_path='',
            static_folder='public',
            template_folder='templates')

app.config['SECRET_KEY'] = 'keepthissecret'

client = pymongo.MongoClient('mongodb+srv://admin:slapbass@cluster0.a6um0.mongodb.net/test')['Tourisit']

shop_db = client['Listings']


class ListingForm(FlaskForm):
    tour_name = StringField('tour_name', validators=[InputRequired(), Length(min=1, max=30,
                                                                             message='Name can only be 30 characters long!')])
    tour_brief = StringField('tour_brief', validators=[InputRequired(), Length(min=1, max=100,
                                                                               message='Brief description can only be 100 characters long!')])
    tour_desc = TextAreaField('tour_desc', validators=[InputRequired()])
    # render_kw will pass in a dictionary.. if you want to render custom css etc..
    # tour_desc = TextAreaField('tour_desc', validators=[InputRequired()], render_kw={"rows": 70, "cols": 11})
    tour_img = FileField('tour_img')
    tour_price = IntegerField('tour_price', validators=[InputRequired(), NumberRange(min=0, max=None,
                                                                                     message='Price cannot be below $0!')])


@app.route('/listings/add', methods=['GET', 'POST'])
def makelisting():
    lForm = ListingForm()
    if request.method == 'POST':
        if lForm.validate_on_submit():
            tour_name = request.form['tour_name']
            brief_desc = request.form['tour_brief']
            detail_desc = request.form['tour_desc']
            tour_img = request.files['tour_img']
            tour_price = request.form['tour_price']
            print(tour_name)

            tour_listing = Listing(tour_name=tour_name, tour_brief=brief_desc, tour_desc=detail_desc,
                                   tour_price=tour_price,
                                   tour_img=tour_img, tg_uid='testing')

            x = tour_listing.return_obj()
            return x
        return render_template('tourGuides/makelisting.html', form=lForm)

    else:
        return render_template('tourGuides/makelisting.html', form=lForm)


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


# CUSTOMERS
# Favourites: Shows all the liked listings
@app.route('/me/favourites')
def favourites():
    return render_template('customer/favourites.html')


# TOUR GUIDES
# Manage Listings: For Tour Guides to Edit/Manage their listings
@app.route('/listings')
def ownlisting():
    return render_template('tourGuides/ownlisting.html', listings=list(shop_db.find()))


# TOUR GUIDES
# Delete Listings: When click on Delete button
@app.route('/listings/delete/<int:id>', methods=['GET', 'POST'])
def deleteList(id):
    listing = shop_db.delete_one({'_id': ObjectId(id)})

    return redirect('/listings')


# TOUR GUIDES
# Edit Listings: When click on own listing to edit
@app.route('/listings/edit/<int:id>', methods=['GET', 'POST'])
def editList(id):
    if request.method == 'POST':
        listing = shop_db.find_one({'_id': ObjectId(id)})

        tour_name = request.form['tour-title']
        tour_brief = request.form['tour-brief']
        tour_desc = request.form['tour-desc']
        tour_img = bytes(request.files['tour-img'].filename)
        listing.tour_img = tour_img
        tour_price = request.form['tour-price']
        updated = {
            "$set": {"tour_name": tour_name, "tour_brief": tour_brief, "tour_desc": tour_desc, "tour_img": tour_img,
                     "tour_price": tour_price}}

        return redirect(f'/discover/{id}')

    else:
        item = Listing.query.filter_by(tour_id=id).first()
        return render_template('tourGuides/editListing.html', listing=item)


# TOUR GUIDES

def img_to_base64(img):
    img = Image.open(img).resize((150, 150))
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str


# Add a Listing: For Tour Guides to add listing
# @app.route('/listings/add', methods=['GET', 'POST'])
# def makelisting():
#     if request.method == 'POST':
#
#         # This should be the tour guide
#         jake = User.query.filter_by(user_name='Jake001').first()
#
#         tour_title = request.form['tour-title']
#         brief_desc = request.form['tour-brief']
#         detail_desc = request.form['tour-desc']
#         tour_img = request.files['tour-img'].filename
#         if tour_img == '':
#             tour_img = str(uuid.uuid1()) + '.jpg'
#         tour_price = request.form['tour-price']
#
#         listing = Listing(tour_name=tour_title, tour_brief=brief_desc, tour_desc=detail_desc, tour_price=tour_price,
#                           tour_img=tour_img, tour_guide=jake)
#
#         db.session.add(listing)
#         db.session.commit()
#         # Replace with success msg
#         return render_template('tourGuides/listing-success.html')
#
#     else:
#         return render_template('tourGuides/makelisting.html', form=ListingForm)


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
