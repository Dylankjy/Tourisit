# Flask imports
# Data Generation
from io import BytesIO

# Database
import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, make_response

# Authentication library
import auth as auth
# Chat Library
import chat as msg

# Custom class imports
from models.Listing import ListingForm, Listing
from models.User import UserForm, BioForm
from models.formatting import JSONEncoder, img_to_base64

from models.Booking import BookingForm, Booking

# For Images
buffered = BytesIO()

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
client = pymongo.MongoClient('mongodb+srv://admin:slapbass@cluster0.a6um0.mongodb.net/test')['Tourisit']

# Initialize all DBs here
shop_db = client['Listings']
user_db = client['Users']
bookings_db = client['Bookings']


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
@app.route('/users', methods=['GET', 'POST'])
def profile():
    bForm = BioForm()
    result = auth.is_auth(True)
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
        return render_template('profile.html', user=item, form=bForm)
    else:
        bForm.bio.default = item['bio']
        bForm.process()
        return render_template('profile.html', user=item, form=bForm)


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
                password = request.form['password']
                email = request.form['email']
                phone_number = request.form['phone_number']
                fb = request.form['fb']
                insta = request.form['insta']
                linkedin = request.form['linkedin']
                updated = {
                    "$set": {"name": name, "password": auth.generate_password_hash(password), "email": email,
                             "phone_number": phone_number,
                             "socialmedia": {"fb": fb, "insta": insta, "linkedin": linkedin}
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
@app.route('/', methods=['GET'])
def home():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return render_template('customer/index-customer.html',
                               listings=list(shop_db.find()), loggedin=False)
    # if logged in
    else:
        print(result)
        return render_template('customer/index-customer.html',
                               listings=list(shop_db.find()), loggedin=True, user=result)


# CUSTOMERS
# Marketplace: Display all listings
@app.route('/discover')
def market():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return render_template('customer/marketplace.html',
                               listings=list(shop_db.find()), loggedin=False)
    # if logged in
    else:
        return render_template('customer/marketplace.html',
                               listings=list(shop_db.find()), loggedin=True, user=result)


# To implement search function
@app.route('/search')
def search():
    all_listings = list(i['tour_name'] for i in shop_db.find())
    # Get the string that is typed in the search bar
    text = request.args['searchListing']
    if text:
        # Get all the listing names from db
        # Get all the listings that fulfil the criteria
        result = [c for c in all_listings if str(text).lower() in c.lower()]
        result_listings = list(shop_db.find({'tour_name': {'$in': result}}))
        for listing in result_listings:
            listing['_id'] = JSONEncoder().encode(listing['_id'])
            listing['tg_uid'] = JSONEncoder().encode(listing['tg_uid'])
            listing['date_created'] = str(listing['date_created'])
            listing['tour_img'] = str(listing['tour_img'])

        return json.dumps({"results": result_listings})


# CUSTOMERS
# Detailed Listing: More detailed listing when listing from M clicked
@app.route('/discover/<tour_id>')
def tourListing(tour_id):
    item = shop_db.find_one({'_id': ObjectId(tour_id)})
    result = auth.is_auth(True)

    #Boolean, will be editable if person is the owner of the listing
    editable = item['tg_uid'] == result['_id']
    # if not logged in
    if not result:
        return render_template('customer/tourListing.html', item=item, loggedin=False, editable=editable)
    # if logged in
    else:
        return render_template('customer/tourListing.html', item=item, loggedin=True, user=result, editable=editable)


# TOUR GUIDES
# Manage Listings: For Tour Guides to Edit/Manage their listings
@app.route('/listings')
def ownlisting():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return render_template('tourGuides/ownlisting.html', listings=None, loggedin=False)
    # if logged in
    else:
        tourGuide_id = result['_id']
        tour_listings = list(shop_db.find({'tg_uid': tourGuide_id}))
        return render_template('tourGuides/ownlisting.html', listings=tour_listings, loggedin=True, user=result)


@app.route('/apis/upImg')
def updateImg():
    text = request.args['currentImg']
    return json.dumps({"results": text})


@app.route('/test/result')
def testing():
    result = auth.is_auth(True)
    id = result['_id']
    print(str(id))
    return str(id)


@app.route('/listings/add', methods=['GET', 'POST'])
def makelisting():
    result = auth.is_auth(True)
    # If result is not None (User is logged in)
    if result:
        lForm = ListingForm()
        if request.method == 'POST':
            if lForm.validate_on_submit():
                tour_name = request.form['tour_name']

                detail_desc = request.form['tour_desc']

                tour_itinerary = request.form.getlist('tour_items_list[]')
                #Convert to a list
                print(tour_itinerary)
                tour_itinerary = tour_itinerary[0].replace("None,", '')
                tour_itinerary = tour_itinerary.replace(",None", '')
                tour_itinerary = tour_itinerary.split('#$%^#,')
                #Remove the special seperators for the last list element
                tour_itinerary[-1] = tour_itinerary[-1].strip('#$%^#')
                #Make sure there is no empty strings
                tour_itinerary = [i for i in tour_itinerary if i.strip() != '']
                print(type(tour_itinerary))
                print(tour_itinerary)

                tour_locations = []
                tour_locations.append(request.form['tour_loc'])

                tour_img = request.files['tour_img']
                img_string = img_to_base64(tour_img)

                tour_revisions = request.form['tour_revisions']

                tour_price = request.form['tour_price']

                tg_uid = result['_id']

                tg_name = result['name']

                print(tour_itinerary)

                tour_listing = Listing(tour_name=tour_name, tour_desc=detail_desc,
                                       tour_price=tour_price,
                                       tour_img=img_string, tg_uid=tg_uid, tg_name=tg_name,
                                       tour_loc=tour_locations, tour_revs=tour_revisions, tour_itinerary=tour_itinerary)

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
    editable = item['tg_uid'] == result['_id']
    if editable == True:
        if request.method == 'POST':
            if lForm.validate_on_submit():
                query_listing = {'_id': ObjectId(id)}
                tour_name = request.form['tour_name']
                detail_desc = request.form['tour_desc']
                tour_itinerary = []
                tour_itinerary.append(request.form['tour_items'])
                tour_locations = []
                tour_locations.append(request.form['tour_loc'])
                tour_img = request.files['tour_img']
                img_string = img_to_base64(tour_img)
                tour_revisions = request.form['tour_revisions']
                tour_price = request.form['tour_price']


                updated = {
                    "$set": {'tour_name':tour_name, 'tour_desc': detail_desc,
                                       'tour_price':tour_price, 'tour_img':img_string,
                                       'tour_loc':tour_locations, 'tour_revs':tour_revisions,'tour_itinerary':tour_itinerary}}

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
    try:
        # Get login status using accessor argument
        result = auth.is_auth(True)
        # if not logged in
        if not result:
            return render_template('customer/allBookings.html', loggedin=False)
        # if logged in
        else:
            return render_template('customer/allBookings.html', loggedin=True, user=result)
    except:
        return 'Error trying to render'


# CUSTOMER
# Individual Bookings
# @app.route('/bookings/<id>')
@app.route('/bookings/id')
def bookings():
    try:
        # Get login status using accessor argument
        result = auth.is_auth(True)
        # if not logged in
        if not result:
            return render_template('customer/booking.html', process_step=1, loggedin=False)
        # if logged in
        else:
            return render_template('customer/booking.html', process_step=1, loggedin=True, user=result)
    except:
        return 'Error trying to render'

# @app.route('/listings/id/booknow')
# def book_now():
#     try:
#         # Get login status using accessor argument
#         result = auth.is_auth(True)
#         # if not logged in
#         if not result:
#             return render_template('customer/book-now.html', loggedin=False)
#         # if logged in
#         else:
#             return render_template('customer/book-now.html', loggedin=True, user=result)
#     except:
#         return 'Error trying to render'

# CUSTOMER
# Book Now Page
@app.route('/discover/<tour_id>/booknow', methods=['GET', 'POST'])
def book_now(tour_id):
    try:
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
                    accept_tnc = request.form["accept_tnc"]
                    print(f"success!{book_date}, at{book_time}, and {accept_tnc}")
                    # booking = Booking(cust_uid=result['_id'], book_date=book_date, book_time=book_time)
                    # # tg_uid, cust_uid, listing_id, book_date, book_time, book_duration, timeline_content, process_step
                    #
                    # print(booking.return_obj())
                    # # bookings_db.insert_one(booking)
                    # # return redirect(url_for('checkout'))

            return render_template('customer/book-now.html', loggedin=True, user=result, form=bookform, item=item)
        # if not logged in
        else:
            return render_template('customer/book-now.html', loggedin=False)
    except:
        return 'Error trying to render'


# CUSTOMER
# Checkout page (placeholder)
# @app.route('/checkout/<id>')
@app.route('/checkout/id')
def checkout():
    try:
        # Get login status using accessor argument
        result = auth.is_auth(True)
        # if not logged in
        if not result:
            return render_template('customer/checkout.html', loggedin=False)
        # if logged in
        else:
            return render_template('customer/checkout.html', loggedin=True, user=result)
    except:
        return 'Error trying to render'


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
            return render_template('tourGuides/allBusinesses.html', loggedin=True, user=result)
    except:
        return 'Error trying to render'


# TOUR GUIDES
# Individual gigs  
# @app.route('/s/businesses/<id>')
@app.route('/s/businesses/id')
def business():
    try:
        # Get login status using accessor argument
        result = auth.is_auth(True)
        # if not logged in
        if not result:
            return render_template('tourGuides/business.html', process_step=4, loggedin=False)
        # if logged in
        else:
            return render_template('tourGuides/business.html', process_step=4, loggedin=True, user=result)
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
    if not result:
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
    if not result:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        return render_template('internal/users.html', loggedin=True, user=result)


# INTERNAL
# Admin Dashboard -- Manage listings
@app.route('/admin/listings')
def adminListings():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        return render_template('internal/listings.html', loggedin=True, user=result)


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
        return render_template('auth/login.html', form=form, denied_access=request.args.get('denied_access'))
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
        # TODO: Add dynamic chat to right side of page! おやすみなさい。。。ｚｚｚZZZ
        chat_list = msg.get_chat_list_for_ui(auth.get_sid(), 'BOOKING')
        print(chat_list)
        return render_template('chat.html', loggedin=True, user=result, list=chat_list)


# MEMBERS
# Chat endpoint
@app.route('/endpoint/chat')
def chatroom_endpoint():
    chat_id = request.args.get('chat_id')
    resp = make_response()
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"

    if auth.is_auth():
        if chat_id:
            sid = auth.get_sid()
            chatroom_data = msg.get_chat_room(sid, chat_id)

            if not chatroom_data:
                resp = make_response('Tourisit API Endpoint - Error 500', 500)
                return resp
            else:
                resp = make_response(JSONEncoder().encode(chatroom_data))
                return resp
        else:
            resp = make_response('Tourisit API Endpoint - Error 400', 400)
            return resp
    else:
        resp = make_response('Tourisit API Endpoint - Error 403', 403)
        return resp


# Run app
if __name__ == '__main__':
    app.run(debug=True)
