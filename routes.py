# Flask imports
# Data Generation
from datetime import datetime
from io import BytesIO

# Database
import bson
import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, make_response, Response

import admin as admin
import auth as auth
# Chat Library
import chat as msg
from models.Booking import BookingForm, CheckoutForm, Booking
from models.Format import JSONEncoder, img_to_base64, formToArray
# Custom class imports
from models.Listing import ListingForm, Listing
from models.Support import SupportForm, Support
from models.User import UserForm, BioForm

# Authentication library

# For Images
buffered = BytesIO()

# db.createUser(
#   {
#     user: "tourisitUser",
#     pwd: "desk-kun_did_nothing_wrong_uwu",
#     roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
#   }
# )

# mongodb://tourisitUser:desk-kun_did_nothing_wrong_uwu@ip.system.gov.hiy.sh:27017


import json

app = Flask(__name__,
            static_url_path='',
            static_folder='public',
            template_folder='templates')

# APP CONFIGS
# REMEMBER TO USE GLOBAL VARIABLE FOR THIS
app.config['SECRET_KEY'] = 'keepthissecret'
# Set file upload limit to 1MB
app.config["MAX_IMAGE_FILESIZE"] = 1 * 1024 * 1024

# CHANGE THE PASSWORD TO A GLOBAL VARIABLE
client = pymongo.MongoClient('mongodb://tourisitUser:desk-kun_did_nothing_wrong_uwu@ip.system.gov.hiy.sh:27017')[
    'Tourisit']

# Initialize all DBs here
shop_db = client['Listings']
user_db = client['Users']
bookings_db = client['Bookings']
support_db = client['Support']


@app.template_filter('timestamp_iso')
def timestamp_iso(s):
    try:
        date = datetime.fromisoformat(s).strftime('%d %B %Y @ %X')
        return date
    except ValueError:
        return 'Unknown'


@app.template_filter('user_pfp')
def user_pfp(uid):
    try:
        query = {
            "_id": ObjectId(uid)
        }
    except bson.errors.InvalidId:
        return ''

    try:
        pfp_data = [i for i in user_db.find(query)][0]["profile_img"]
    except IndexError:
        pfp_data = ''

    return pfp_data


@app.template_filter('user_name')
def user_name(uid):
    try:
        query = {
            "_id": ObjectId(uid)
        }
    except bson.errors.InvalidId:
        return ''

    try:
        tg_name = [i for i in user_db.find(query)][0]["name"]
    except IndexError:
        tg_name = ''

    return tg_name


# @app.before_request
# def before_request_callback():
#     if auth.is_auth(True)["account_mode"] == -1:
#         return render_template('onboarding/welcomepage.html')


# @app.template_filter('parse_uid_name')
# def parse_uid_name(uid):
#     query = {
#         "_id": ObjectId(uid)
#     }
#     try:
#         name = user_db.find_one(query)[0]["name"]
#     except:
#         name = ''
#     return name


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
@app.route('/support', methods=['GET', 'POST'])
def support():
    result = auth.is_auth(True)
    if result:
        sForm = SupportForm()
        if request.method == 'POST':
            if sForm.validate_on_submit():
                uid = result['_id']
                support_type = request.form['support_type']
                link = request.form['link']
                content = request.form['content']
                support_request = Support(uid=uid, support_type=support_type, link=link, content=content)
                support_info = support_request.return_obj()
                print(support_info)
                support_db.insert_one(support_info)
                return render_template('success-user.html', user=result)
            return render_template('helpdesk.html', user=result, form=sForm, loggedin=True)
        else:
            return render_template('helpdesk.html', user=result, form=sForm, loggedin=True)
    else:
        return 'Need to login/create account first!'


# SHARED
# User profile
# @app.route('/users/<id>)
@app.route('/users', methods=['GET', 'POST'])
def profile():
    bForm = BioForm()
    result = auth.is_auth(True)
    if result:
        id = result["_id"]
        item = user_db.find_one({'_id': ObjectId(id)})
        if request.method == 'POST':
            if bForm.validate_on_submit():
                query_user = {'_id': ObjectId(id)}
                bio = request.form["bio"]
                updated = {
                    "$set": {"bio": bio}
                }
                user_db.update_one(query_user, updated)
                # return render_template('profile.html', user=item, form=bForm)
            return render_template('profile.html', user=item, form=bForm, loggedin=True)
        else:
            bForm.bio.default = item['bio']
            bForm.process()
            return render_template('profile.html', user=item, form=bForm, loggedin=True)
    else:
        return render_template('profile.html', form=bForm, logged_in=False)


# SHARED
# User account settings
@app.route('/me/settings', methods=['GET', 'POST'])
def accountinfo():
    uForm = UserForm()
    result = auth.is_auth(True)
    # If user is logged in and makes changes to the settings
    if result:
        id = result["_id"]
        item = user_db.find_one({'_id': ObjectId(id)})
        if request.method == 'POST':
            if uForm.validate_on_submit():
                query_user = {'_id': ObjectId(id)}
                name = request.form['name']
                email = request.form['email']
                phone_number = request.form['phone_number']
                fb = request.form['fb']
                insta = request.form['insta']
                linkedin = request.form['linkedin']
                account_mode = request.form['account_mode']
                password = request.form['password']
                #If password is same
                if password == '':
                    updated = {
                        "$set": {"name": name,
                                 "email": email, "phone_number": phone_number,
                                 "socialmedia": {"fb": fb, "insta": insta, "linkedin": linkedin},
                                 "account_mode": account_mode
                                 }
                    }
                else:
                    updated = {
                        "$set": {"name": name, "password": auth.generate_password_hash(password),
                                 "email": email, "phone_number": phone_number,
                                 "socialmedia": {"fb": fb, "insta": insta, "linkedin": linkedin},
                                 "account_mode": account_mode
                                 }
                    }
                user_db.update_one(query_user, updated)
                return render_template('success-user.html', user=item, id=id, loggedin=True)
            return render_template('setting.html', user=item, form=uForm, loggedin=True)

        # Else if not logged in
        else:
            return render_template('setting.html', user=item, form=uForm, loggedin=True)

    else:
        # Render the pls log in template here
        return 'Pls log in'


@app.route('/me/billing')
def accountbilling():
    try:
        return render_template('billing.html')
    except:
        return 'Error trying to render'


# --------------------------------------

# ALEX

# CUSTOMERS
# Home page
@app.route('/')
def home():
    query = {}
    all_listings = [i for i in shop_db.find(query)]
    all_listings.reverse()
    shown_listings = []

    for i in range(6):
        shown_listings.append(all_listings[i])

    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return render_template('customer/index-customer.html',
                               item_list=shown_listings, loggedin=False)
    # if logged in
    else:
        return render_template('customer/index-customer.html',
                               item_list=shown_listings, loggedin=True, user=result)


# CUSTOMERS
# Marketplace: Display all listings
@app.route('/discover')
def market():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    query = {}
    all_listings = [i for i in shop_db.find(query)]
    # if not logged in
    if not result:
        return render_template('customer/marketplace.html',
                               listings=list(shop_db.find()), loggedin=False, item_list=all_listings)
    # if logged in
    else:
        return render_template('customer/marketplace.html',
                               listings=list(shop_db.find()), loggedin=True, user=result, item_list=all_listings)


# To implement search function
@app.route('/endpoint/search')
def search():
    all_listings = list(i['tour_name'] for i in shop_db.find())
    # Get the string that is typed in the search bar

    try:
        text = request.args['query']
    except KeyError:
        text = None

    if text != None:
        # Get all the listing names from db
        # Get all the listings that fulfil the criteria

        result = [c for c in all_listings if str(text).lower() in c.lower()]
        result_listings = list(shop_db.find({'tour_name': {'$in': result}}))

        resp = make_response()
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"

        shard_payload = render_template('components/listing-card.html', item_list=result_listings)

        resp = Response(
            response=JSONEncoder().encode({
                "data": shard_payload
            }),
            mimetype='application/json',
            status=200
        )

        return resp
    else:
        resp = make_response('Tourisit API Endpoint - Error 400', 400)
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        return resp


# CUSTOMERS
# Detailed Listing: More detailed listing when listing from Marketplace clicked
@app.route('/discover/<tour_id>')
def tourListing(tour_id):
    # Dynamically load the user data (From the database) so if user info changes, all will change too
    item = shop_db.find_one({'_id': ObjectId(tour_id)})
    tg_id = item['tg_uid']
    result = auth.is_auth(True)
    userData = user_db.find_one({'_id': tg_id})

    # Boolean, will be editable if person is the owner of the listing
    if result:
        editable = item['tg_uid'] == result['_id']
    else:
        editable = False
    # if not logged in
    if not result:
        return render_template('customer/tourListing.html', item=item, loggedin=False, editable=editable,
                               userData=userData)
    # if logged in
    else:
        return render_template('customer/tourListing.html', item=item, loggedin=True, user=result, editable=editable,
                               userData=userData)


# TOUR GUIDES
# Manage Listings: For Tour Guides to Edit/Manage their listings
@app.route('/listings')
def ownlisting():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # Get the data of the current user
    userData = user_db.find_one({'_id': result['_id']})
    # item = shop_db.find_one({'_id': ObjectId(tour_id)})
    # tg_id = item['tg_uid']
    # result = auth.is_auth(True)
    # userData = user_db.find_one({'_id': tg_id})

    # if not logged in
    if not result:
        return render_template('tourGuides/ownlisting.html', listings=None, loggedin=False)
    # if logged in
    else:
        tourGuide_id = result['_id']
        tour_listings = list(shop_db.find({'tg_uid': tourGuide_id}))
        return render_template('tourGuides/ownlisting.html', listings=tour_listings, loggedin=True, user=result,
                               userData=userData)


@app.route('/apis/upImg')
def updateImg():
    text = request.args['currentImg']
    return json.dumps({"results": text})


@app.route('/test/result')
def testing():
    listing = list(shop_db.find({'tour_name': 'new'}))
    items = listing[0]['tour_itinerary']
    x = json.dumps(items)
    print(type(x))
    return x
    # result = auth.is_auth(True)
    # lForm = ListingForm()
    # return render_template('tourGuides/makelisting.html', form=lForm, user=result)


@app.route('/listings/add', methods=['GET', 'POST'])
def makelisting():
    result = auth.is_auth(True)
    # If result is not None (User is logged in)
    if result:
        userData = user_db.find_one({'_id': result['_id']})
        # Use this, don't hard code the values
        userImg = userData['profile_img']
        userName = userData['name']

        print(f'User img is: {userImg}')
        lForm = ListingForm()
        if request.method == 'POST':
            if lForm.validate_on_submit():
                tour_name = request.form['tour_name']

                detail_desc = request.form['tour_desc']

                itinerary_form_list = request.form.getlist('tour_items_list[]')
                tour_itinerary = formToArray(itinerary_form_list)

                locations_form_list = request.form.getlist('tour_locations_list[]')
                tour_locations = formToArray(locations_form_list)

                tour_img = request.files['tour_img']
                img_string = img_to_base64(tour_img)

                tour_revisions = request.form['tour_revisions']

                tour_price = request.form['tour_price']

                tg_uid = result['_id']

                print(tour_itinerary)

                tour_listing = Listing(tour_name=tour_name, tour_desc=detail_desc,
                                       tour_price=tour_price,
                                       tour_img=img_string, tg_uid=tg_uid,
                                       tour_location=tour_locations, tour_revs=tour_revisions,
                                       tour_itinerary=tour_itinerary)

                listingInfo = tour_listing.return_obj()
                print(listingInfo)
                shop_db.insert_one(listingInfo)

                return render_template('tourGuides/listing-success.html', user=result)
            return render_template('tourGuides/makelisting.html', form=lForm, user=result)

        else:
            return render_template('tourGuides/makelisting.html', form=lForm, user=result)
    else:
        return 'Need to login/create account first!'


# TOUR GUIDES
# Edit Listings: When click on own listing to edit
@app.route('/listings/edit/<id>', methods=['GET', 'POST'])
def editListing(id):
    result = auth.is_auth(True)
    lForm = ListingForm()
    item = shop_db.find_one({'_id': ObjectId(id)})
    itinerary_list = json.dumps(item['tour_itinerary'])
    editable = item['tg_uid'] == result['_id']
    if editable == True:
        if request.method == 'POST':
            if lForm.validate_on_submit():
                query_listing = {'_id': ObjectId(id)}
                tour_name = request.form['tour_name']

                detail_desc = request.form['tour_desc']

                itinerary_form_list = request.form.getlist('tour_items_list[]')
                tour_itinerary = formToArray(itinerary_form_list)

                locations_form_list = request.form.getlist('tour_locations_list[]')
                tour_locations = formToArray(locations_form_list)

                tour_revisions = request.form['tour_revisions']

                tour_price = request.form['tour_price']

                tg_uid = result['_id']

                tour_img = request.files['tour_img']
                img_string = img_to_base64(tour_img)
                # If there's no change to image (User doesnt upload new image), keep the current image
                print('Img string is:' + img_string)
                if img_string == '':
                    img_string = item['tour_img']
                    print('This fired!')
                    # Don't update the tour image
                    updated = {
                        "$set": {'tour_name': tour_name, 'tour_desc': detail_desc,
                                 'tour_price': tour_price, 'tour_location': tour_locations,
                                 'tour_revisions': tour_revisions, 'tour_itinerary': tour_itinerary}}

                else:
                    updated = {
                        "$set": {'tour_name': tour_name, 'tour_desc': detail_desc,
                                 'tour_price': tour_price, 'tour_img': img_string,
                                 'tour_location': tour_locations, 'tour_revisions': tour_revisions,
                                 'tour_itinerary': tour_itinerary}}

                shop_db.update_one(query_listing, updated)

                return render_template('tourGuides/editing-success.html', id=id, user=result)
            lForm.tour_desc.default = item['tour_desc']
            lForm.process()
            return render_template('tourGuides/editListing.html', listing=item, form=lForm, user=result)

        else:
            # print(item['tour_name'])
            lForm.tour_desc.default = item['tour_desc']
            lForm.process()
            return render_template('tourGuides/editListing.html', listing=item, form=lForm, user=result)
    else:
        return 'Not allowed to edit!'


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
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return render_template('customer/favourites.html', loggedin=False)
    # if logged in
    else:
        return render_template('customer/favourites.html', loggedin=True, user=result)


# --------------------------------------

# Chlorine (Cl) - 17, 35.5 [Halogen]

# CUSTOMER
# Your Bookings: Access all bookings
@app.route('/bookings')
def all_bookings():
    # try:
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return render_template('customer/allBookings.html', loggedin=False)
    # if logged in
    else:
        cust_uid = result['_id']
        booking_list = list(bookings_db.find({'cust_uid': cust_uid}))
        listings = []
        for item in booking_list:
            listings.append(shop_db.find_one({'_id': item['listing_id']}))
        booking_list.reverse()
        listings.reverse()
        return render_template('customer/allBookings.html', booking_list=booking_list, listings=listings, loggedin=True,
                               user=result)


# except:
#     return 'Error trying to render'


# CUSTOMER
# Individual Bookings
# @app.route('/bookings/<id>')
@app.route('/bookings/<book_id>', methods=['GET', 'POST'])
def bookings(book_id):
    # try:
    booking = bookings_db.find_one({'_id': ObjectId(book_id)})
    tour = shop_db.find_one({'_id': booking['listing_id']})
    print(booking)
    print(tour)
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return render_template('customer/booking.html', loggedin=False)
    # if logged in
    else:
        if request.method == 'POST':
            print("yes")
            # if request.form['TourComplete_submit'] == 'TourComplete':
            #     update_booking = { "$set": { "process_step": 7 } }
            #     bookings_db.update_one(booking, update_booking)

        return render_template('customer/booking.html',
                               process_step=booking['process_step'],
                               booking=booking,
                               tour=tour,
                               loggedin=True,
                               user=result)


# except:
#     return 'Error trying to render'


# CUSTOMER
# Book Now Page
@app.route('/discover/<tour_id>/booknow', methods=['GET', 'POST'])
def book_now(tour_id):
    # try:
    item = shop_db.find_one({'_id': ObjectId(tour_id)})
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if logged in
    if result:
        bookform = BookingForm()
        if request.method == 'POST':
            if bookform.validate_on_submit():
                book_date = request.form["book_date"]
                book_time = request.form["book_time"]
                booking = Booking(tg_uid=item['tg_uid'], cust_uid=result['_id'], listing_id=item['_id'],
                                  book_date=book_date, book_time=book_time, book_baseprice=item['tour_price'],
                                  book_customfee=0, book_duration="", timeline_content=[],
                                  process_step=5)
                inserted_booking = bookings_db.insert_one(booking.return_obj())
                book_id = inserted_booking.inserted_id
                return redirect(url_for('checkout', book_id=book_id))

        return render_template('customer/book-now.html', loggedin=True, user=result, form=bookform, item=item,
                               tour_id=tour_id)
    # if not logged in
    else:
        return render_template('customer/book-now.html', loggedin=False)


# except:
#     return 'Error trying to render'


# CUSTOMER
# Checkout page (placeholder)
@app.route('/checkout/<book_id>', methods=['GET', 'POST'])
def checkout(book_id):
    # try:
    booking = bookings_db.find_one({'_id': ObjectId(book_id)})
    form = CheckoutForm()
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if logged in
    if result:
        if request.method == 'POST':
            if form.validate_on_submit():
                if booking['process_step'] == 5:
                    update_booking = {"$set": {"process_step": 6}}
                    bookings_db.update_one(booking, update_booking)
                    return redirect(url_for('bookings', book_id=str(book_id)))
                elif booking['process_step'] == 0:
                    update_booking = {"$set": {"process_step": 1}}
                    bookings_db.update_one(booking, update_booking)

                else:
                    print("Error occurred while trying to pay.")

        return render_template('customer/checkout.html', loggedin=True, user=result, booking=booking, form=form,
                               book_id=book_id)
    # if not logged in
    else:
        return render_template('customer/checkout.html', loggedin=False)


# except:
#     return 'Error trying to render (checkout)'


# TOUR GUIDES
# My Businesses: Access all gigs
@app.route('/s/businesses')
def all_businesses():
    try:
        # Get login status using accessor argument
        result = auth.is_auth(True)
        # if not logged in
        if not result:
            return render_template('tourGuides/allBusinesses.html', loggedin=False)
        # if logged in
        else:
            tg_uid = result['_id']
            booking_list = list(bookings_db.find({'cust_uid': tg_uid}))
            listings = []
            for item in booking_list:
                listings.append(shop_db.find_one({'_id': item['listing_id']}))
            booking_list.reverse()
            listings.reverse()
            return render_template('tourGuides/allBusinesses.html', booking_list=booking_list, listings=listings,
                                   loggedin=True,
                                   user=result)
    except:
        return 'Error trying to render'


# TOUR GUIDES
# Individual gigs  
# @app.route('/s/businesses/<id>')
@app.route('/s/businesses/<book_id>')
def business(book_id):
    try:
        booking = bookings_db.find_one({'_id': ObjectId(book_id)})
        tour = shop_db.find_one({'_id': booking['listing_id']})
        # Get login status using accessor argument
        result = auth.is_auth(True)
        # if not logged in
        if not result:
            return render_template('tourGuides/business.html', loggedin=False)
        # if logged in
        else:
            print(booking)
            print(tour)
            print(booking['process_step'])
            return render_template('tourGuides/business.html',
                                   process_step=booking['process_step'],
                                   booking=booking,
                                   tour=tour,
                                   loggedin=True,
                                   user=result)
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
# Dashboard
@app.route('/s/dashboard')
def sellerDashboard():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        return render_template('tourGuides/dashboard.html', loggedin=True, user=result)


# INTERNAL
# Admin Dashboard -- Private internal shit
@app.route('/admin')
def adminDashboard():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result or result['account_type'] != 1:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        return render_template('internal/dashboard.html', loggedin=True, user=result)


# INTERNAL
# Admin Dashboard -- Manage users
@app.route('/admin/users')
def adminUsers():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result or result['account_type'] != 1:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        user_accounts = admin.list_user_accounts()
        return render_template('internal/users.html', loggedin=True, user=result, user_list=user_accounts)


# INTERNAL
# Admin Dashboard -- Manage listings
@app.route('/admin/listings')
def adminListings():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result or result['account_type'] != 1:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        return render_template('internal/listings.html', loggedin=True, user=result, listing=admin.list_listings())


# SHARED
# Login Page
@app.route('/login', methods=['POST', 'GET'])
def login():
    # Login form
    form = auth.LoginForm()

    # If user is NOT logged in
    if not auth.is_auth():
        # Do if POST response // Form submission
        if form.validate_on_submit():
            email = form.data['email']
            password = form.data['password']

            # login_account implements auth
            result = auth.login_account(email, password)

            # Check for response from auth handler
            if not result:
                # If fail, show failure modal
                return render_template('auth/login.html', form=form, acc_login_failed=True)
            elif result == "UNVERIFIED":
                return redirect(url_for('signup', unverified_email_ref=True, email=email))
            else:
                # If pass, set cookie and redirect
                resp = redirect(url_for('home'))
                resp.set_cookie('tourisitapp-sid', result)
                # resp.set_cookie('tourisitapp-uid', auth.get_user_id(result))
                return resp

        # If GET request // Show page
        return render_template('auth/login.html', form=form, denied_access=request.args.get('denied_access'),
                               verification_code_OK=request.args.get('verification_code_OK'),
                               verification_code_denied=request.args.get('verification_code_denied')
                               )
    # If user is ALREADY logged in
    else:
        return redirect(url_for('home'))


# SHARED
# Sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Sign up form
    signup_form = auth.SignupForm()
    resend_email_form = auth.ResendEmailForm()

    # Check was this a ref from login because user hasn't gotten their email verified.
    if request.args.get('unverified_email_ref') == "True" and request.args.get('email') is not None:
        return render_template('auth/signup.html', signupform=signup_form, resend_email=resend_email_form,
                               acc_creation=True, email=request.args.get('email'))

    # If user is NOT logged in
    if not auth.is_auth():
        # Do if POST response // Form submission
        if signup_form.validate_on_submit():
            name = signup_form.data['full_name']
            email = signup_form.data['email']
            password = signup_form.data['password']

            # create_account implements auth
            if auth.create_account(name, password, email):
                return render_template('auth/signup.html', signupform=signup_form, resend_email=resend_email_form,
                                       acc_creation=True, email=email)
            else:
                return render_template('auth/signup.html', signupform=signup_form, exist=True, email=email)

        # If GET request // Show page
        return render_template('auth/signup.html', signupform=signup_form, resend_email=resend_email_form,
                               newEmailSent=request.args.get('email_sent'))
    # If user is ALREADY logged in
    else:
        return redirect(url_for('home'))


@app.route('/endpoint/resendEmail', methods=['POST'])
def resend_email():
    resend_email_form = auth.ResendEmailForm()
    # if resend_email_form.validate_on_submit():
    email = resend_email_form.data["email"]

    # if auth.get_sid() is not None:
    #     sid = auth.get_sid()
    #     if auth.send_confirmation_email(sid, None):
    #         print("Email sent via SID")
    #         return redirect(url_for('signup', email_sent=True))

    if email is not None:
        if auth.send_confirmation_email(None, email):
            return redirect(url_for('signup', email_sent=True))


# MEMBERS
# Logout page
@app.route('/logout')
def logout():
    if auth.get_sid() is not None:
        if request.args.get('all'):
            auth.logout_account(auth.get_sid(), True)
        else:
            auth.logout_account(auth.get_sid())
        resp = make_response(render_template('auth/logout.html'))
        resp.set_cookie('tourisitapp-sid', '', expires=0)
        # resp.set_cookie('tourisitapp-uid', '', expires=0)
        return resp
    else:
        return redirect(url_for('home'))


# SHARED
# Chats: Render individual chats -- Stolen from Chloe
@app.route('/chat')
def chat():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        chat_list = msg.get_chat_list_for_ui(auth.get_sid(), 'BOOKING')
        return render_template('chat.html', loggedin=True, user=result, list=chat_list, chatroom_display=False,
                               not_found=request.args.get('not_found'))


@app.route('/chat/<room_id>', methods=['GET', 'POST'])
def chat_room(room_id):
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        # Chat form
        chat_form = msg.ChatForm()

        if chat_form.validate_on_submit():
            # print(chat_form.data["message"])
            print(msg.add_message(room_id, auth.get_sid(), chat_form.data["message"]))

        chat_list = msg.get_chat_list_for_ui(auth.get_sid(), 'BOOKING')
        chat_room_messages = msg.get_chat_room(auth.get_sid(), room_id)

        if not chat_room_messages:
            return redirect(url_for('chat', not_found=True))

        return render_template('chat.html', loggedin=True, user=result, list=chat_list, form=chat_form,
                               chatroom_display=chat_room_messages["chatroom"],
                               chatroom_names=chat_room_messages["names"],
                               selected_chatroom=ObjectId(room_id))


# MEMBERS
# Chat endpoint
@app.route('/endpoint/chat')
def chatroom_endpoint():
    chat_id = request.args.get('chat_id')
    resp = make_response()
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"

    if auth.is_auth():
        if chat_id:
            chat_room_messages = msg.get_chat_room(auth.get_sid(), chat_id)

            if not chat_room_messages:
                resp = make_response('Tourisit API Endpoint - Error 500', 500)
                return resp
            else:
                shard_payload = render_template('components/shards/msg.html',
                                                chatroom_display=chat_room_messages["chatroom"])
                resp = Response(
                    response=JSONEncoder().encode({
                        "data": shard_payload
                    }),
                    mimetype='application/json',
                    status=200
                )
                return resp
        else:
            resp = make_response('Tourisit API Endpoint - Error 400', 400)
            return resp
    else:
        resp = make_response('Tourisit API Endpoint - Error 403', 403)
        return resp


# Email confirmation endpoint:
@app.route('/endpoint/email_confirmation')
def email_confirmation_endpoint():
    email_token = request.args.get('token')
    if auth.verify_remove_token("email_verification", email_token):
        return redirect(url_for('login', verification_code_OK=True))
    else:
        return redirect(url_for('login', verification_code_denied=True))


# Run app
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
