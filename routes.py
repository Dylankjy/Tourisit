# Flask imports
# Data Generation
import json
import os
from datetime import datetime
from io import BytesIO
# Database
from threading import Thread

import bson
import pymongo
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, make_response, Response, send_from_directory, \
    abort

import admin as admin
import auth as auth
# Chat Library
import chat as msg
# Custom class imports
import dashboard
from models.Booking import Booking, BookingForm, CheckoutForm, AddInfoForm, RevisionForm, RequirementsForm, EditPlan
from models.Format import JSONEncoder, img_to_base64, formToArray, sortDays, file_to_base64
from models.Listing import ListingForm, Listing
from models.Review import ReviewForm, Review
from models.Support import SupportForm, Support, StatusForm
from models.Transaction import Transaction
from models.User import BioForm, PasswordForm, UserForm

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


app = Flask(__name__,
            static_url_path='',
            static_folder='public',
            template_folder='templates')

# APP CONFIGS
# REMEMBER TO USE GLOBAL VARIABLE FOR THIS
app.config['SECRET_KEY'] = 'keepthissecret'
# Set file upload limit to 1MB
# WILL RETURN 413 ERROR IF THE UPLOADED SIZE IS MORE THAN 5MB
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

# CHANGE THE PASSWORD TO A GLOBAL VARIABLE
client = pymongo.MongoClient(
    'mongodb://tourisitUser:desk-kun_did_nothing_wrong_uwu@ip.system.gov.hiy.sh:27017', maxPoolSize=None)['Tourisit']

# Initialize all DBs here
shop_db = client['Listings']
user_db = client['Users']
bookings_db = client['Bookings']
support_db = client['Support']
transaction_db = client['Transactions']
reviews_db = client['Reviews']
chats_db = client['Chats']
dashboard_db = client['Dashboard']

# Good Stuff
# return redirect(url_for('login', denied_access=True))
# message = 'No listings yet!'
# return redirect(url_for('show_user_message', message=message))

@app.template_filter('timestamp_iso')
def timestamp_iso(s):
    try:
        date = datetime.fromisoformat(s).strftime('%d %B %Y @ %X')
        return date
    except ValueError:
        return 'Unknown'

# ========= For tour guide dashboards =========
# By touching this section, you fully agree to be executed if anything breaks here.
@app.template_filter('stars_to_percentage')
def stars_to_percentage(stars):
    return 100 * (stars / 5)

@app.template_filter('earning_average_month')
def earning_average_month(list):
    total = 0

    for i in list:
        total += i['total']

    return total / 5

@app.template_filter('value_difference_earnings')
def value_difference_earnings(list):
    diff = list[5]['total'] - list[4]['total']
    if list[5]['total'] > list[4]['total']:
        neg_pos = True
    else:
        neg_pos = False
    return [diff, neg_pos]

@app.template_filter('value_difference_stars')
def value_difference_stars(list):
    diff = list[5]['stars'] - list[4]['stars']
    if list[5]['stars'] > list[4]['stars']:
        neg_pos = True
    else:
        neg_pos = False
    return [diff / 5 * 100, neg_pos]

# ========= END OF SECTION =========


@app.template_filter('user_pfp')
def user_pfp(uid):
    try:
        query = {
            "_id": ObjectId(uid)
        }
    except bson.errors.InvalidId:
        return ''

    try:
        pfp_data = user_db.find(query)[0]["profile_img"]
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

uwu_face = file_to_base64('public/imgs/uwu.png')

@app.route('/testImg', methods=['GET', 'POST'])
def test_img():
    return render_template(
        'tourGuides/testImg.html',
        user=None,
        imgBase64=uwu_face)

# Use this to display messages to user
# I.e if user is searching for a listing that doesn't exist, then say 'Listing does not exist' message
@app.route('/showMsg/<message>')
def show_user_message(message):
    result = auth.is_auth(True)
    if result:
        return render_template('show_msg.html', message=message, user=result, loggedin=True)
    return render_template('show_msg.html', message=message)

    # USAGE
    # Create the message, then redirect to showMsg page where message is passed as parameter
    # message = 'No listings yet!'
    # return redirect(url_for('show_user_message', message=message))

# --------------------------------------

# AMY

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
                support_request = Support(
                    uid=uid,
                    support_type=support_type,
                    link=link,
                    content=content
                )
                support_info = support_request.return_obj()
                support_db.insert_one(support_info)

            else:
                return render_template(
                    'helpdesk.html',
                    user=result,
                    form=sForm,
                    loggedin=True)

        return render_template(
            'helpdesk.html',
            user=result,
            form=sForm,
            loggedin=True)
    else:
        return redirect(url_for('login', denied_access=True))

# SHARED
# User profile
@app.route('/users/<user_id>/profile', methods=['GET', 'POST'])
def profile(user_id):
    bForm = BioForm()
    # Find who is it from user_id
    person = user_db.find_one({'_id': ObjectId(user_id)})
    result = auth.is_auth(True)
    items = list(shop_db.find({'tg_uid': ObjectId(user_id)}))[:3]
    # Find who is it from result
    if result:
        # Boolean, will be editable if person is the owner of the profile
        editable = person['_id'] == result['_id']
        profile_img = result['profile_img']
        if request.method == 'POST':
            if bForm.validate_on_submit():
                query_user = {'_id': ObjectId(result['_id'])}
                bio = request.form["bio"]
                updated = {
                    "$set": {"bio": bio}
                }
                user_db.update_one(query_user, updated)
                return redirect(url_for('profile', user_id=person['_id']))
            return render_template(
                'profile.html',
                user=result,
                person=person,
                form=bForm,
                loggedin=True,
                editable=editable,
                profile_img=profile_img,
                item_list=items
            )
        else:
            return render_template(
                'profile.html',
                user=result,
                person=person,
                form=bForm,
                loggedin=True,
                editable=editable,
                profile_img=profile_img,
                item_list=items
            )
    # if not result:
    else:
        editable = False
        profile_img = person['profile_img']
        print(result)
        print(person)
        print(person['name'])
        return render_template(
            'profile.html',
            form=bForm,
            logged_in=False,
            user=result,
            person=person,
            editable=editable,
            profile_img=profile_img,
            item_list=items
        )

# SHARED
# USER SETTINGS AND CHANGE PASSWORD
@app.route('/me/settings', methods=['GET', 'POST'])
def accountinfo():
    uForm = UserForm()
    pForm = PasswordForm()
    result = auth.is_auth(True, True)
    # If user is logged in and makes changes to the settings
    if result:
        id = result["_id"]
        item = user_db.find_one({'_id': ObjectId(id)})
        if request.method == 'POST':
            if "submit-setting" in request.form and uForm.validate_on_submit():
                query_user = {'_id': ObjectId(id)}
                account_mode = int(request.form['account_mode'])
                name = request.form['name']
                profile_img = request.files['profile_img']
                img_string = img_to_base64(profile_img)
                email = request.form['email']
                phone_number = request.form['phone_number']
                fb = request.form['fb']
                insta = request.form['insta']
                linkedin = request.form['linkedin']
                if img_string == '':
                    img_string = item['profile_img']
                    updated = {
                        "$set": {
                            "name": name,
                            "profile_img": img_string,
                            "email": email,
                            "phone_number": phone_number,
                            "socialmedia": {
                                "fb": fb,
                                "insta": insta,
                                "linkedin": linkedin},
                            "account_mode": account_mode
                        }
                    }
                else:
                    updated = {
                        "$set": {
                            "name": name,
                            "profile_img": img_string,
                            "email": email,
                            "phone_number": phone_number,
                            "socialmedia": {
                                "fb": fb,
                                "insta": insta,
                                "linkedin": linkedin},
                            "account_mode": account_mode
                        }
                    }

                user_db.update_one(query_user, updated)
                return render_template(
                    'success-user.html', user=item, id=id, loggedin=True)

            elif "submit-change-pass" in request.form and pForm.validate_on_submit():
                query_user = {'_id': ObjectId(id)}
                old_password = request.form['old_password']
                password = request.form['password']
                confirm = request.form['confirm']
                checker = auth.check_password_correlate(old_password, result['password'])
                if checker:
                    updated = {
                        "$set": {
                            "password": auth.generate_password_hash(password)
                        }
                    }
                    user_db.update_one(query_user, updated)
                    return render_template(
                        'success-support.html', user=item, id=id, loggedin=True)
                else:
                    return render_template('setting.html', user=item, id=id, loggedin=True)
            return render_template(
                'setting.html',
                user=item,
                form=uForm,
                form1=pForm,
                loggedin=True)

        # Else if not POST
        else:
            return render_template(
                'setting.html',
                user=item,
                form=uForm,
                form1=pForm,
                loggedin=True)

    else:
        # Render the pls log in template here
        return redirect(url_for('login', denied_access=True))

# SHARED
# Change ticket status
@app.route('/admin/tickets', methods=['GET', 'POST'])
def adminTickets():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    sForm = StatusForm()
    # if not logged in
    if not result or result['account_type'] != 1:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        if 'change-status' in request.form and request.method == 'POST':
            if sForm.validate_on_submit():
                tid = request.form['id']
                query_ticket = {'_id': ObjectId(tid)}
                status = request.form['status']
                updated = {
                    "$set": {
                        "status": status
                    }
                }
                print(admin.list_tickets())
                support_db.update_one(query_ticket, updated)

                return render_template(
                    'internal/tickets.html',
                    loggedin=True,
                    user=result,
                    tickets=admin.list_tickets(),
                    form=sForm
                )
            return render_template(
                'internal/tickets.html',
                loggedin=True,
                user=result,
                tickets=admin.list_tickets(),
                form=sForm
            )
        else:
            return render_template(
                'internal/tickets.html',
                loggedin=True,
                user=result,
                tickets=admin.list_tickets(),
                form=sForm
            )

# ALEX

# CUSTOMERS
# Home page
@app.route('/')
def home():
    # Get the display items first
    query = {'tour_visibility': 1}
    all_listings = [i for i in shop_db.find(query)]

    if len(all_listings) >= 6:
        all_listings.reverse()
        shown_listings = []

        for i in range(6):
            shown_listings.append(all_listings[i])

    else:
        message = 'No listings yet!'
        return redirect(url_for('show_user_message', message=message))

    # Get login status using accessor argument
    result = auth.is_auth(True)
    if result:
        user_mode = user_db.find_one({'_id': ObjectId(result['_id'])})['account_mode']

        if (user_mode == -1):
            return redirect(url_for('setAccType'))

            # if logged in
        return render_template(
            'customer/index-customer.html',
            item_list=shown_listings,
            loggedin=True,
            user=result)

    return render_template('customer/index-customer.html',
                           item_list=shown_listings, loggedin=False)

# CUSTOMERS
# Marketplace: Display all listings
@app.route('/discover')
def market():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    query = {'tour_visibility': 1}
    all_listings = [i for i in shop_db.find(query)]
    # if not logged in
    if not result:
        return render_template(
            'customer/marketplace.html',
            listings=list(
                shop_db.find()),
            loggedin=False,
            item_list=all_listings)

    # if logged in
    return render_template(
        'customer/marketplace.html',
        listings=list(
            shop_db.find(query)),
        loggedin=True,
        user=result,
        item_list=all_listings)

# To implement search function
@app.route('/endpoint/search')
def search():
    query = {'tour_visibility': 1}
    all_listings = list(i['tour_name'] for i in shop_db.find(query))
    # Get the string that is typed in the search bar

    try:
        text = request.args['query']
    except KeyError:
        text = None

    if text is not None:
        # Get all the listing names from db
        # Get all the listings that fulfil the criteria

        result = [c for c in all_listings if str(text).lower() in c.lower()]
        result_listings = list(shop_db.find({'tour_name': {'$in': result}}))

        resp = make_response()
        resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"

        shard_payload = render_template(
            'components/listing-card.html',
            item_list=result_listings)

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

@app.route('/discover/random')
def randomListing():
    query = [{"$match": {"tour_visibility": 1}},
             {"$sample": {"size": 1}}]
    random_listing = list(shop_db.aggregate(query))[0]
    # Extract the random_id so you can use it to render the discover page
    random_tour_id = random_listing['_id']
    return redirect(url_for('tourListing', tour_id=random_tour_id))

# CUSTOMERS
# Detailed Listing: More detailed listing when listing from Marketplace clicked
@app.route('/discover/<tour_id>')
def tourListing(tour_id):
    # Note that there are 2 users here. The tour guide and the person who is logged in
    # Settle the loading of item first, then settle the logged in user part (Checking of wishlist)

    item = shop_db.find_one({'_id': ObjectId(tour_id)})
    # If item exists
    if item:
        result = auth.is_auth(True)
        display_listing = item['tour_visibility'] == 1
        if result:
            # Boolean, will be editable if person is the owner of the listing
            editable = item['tg_uid'] == result['_id']
            # tg_id = item['tg_uid']
            # tg_userData = user_db.find_one({'_id': tg_id})

            # If listing is viewable, then allow it to be rendered
            # However, if the listing is not viewable, it should still be viewable to the tour guide who created it
            if display_listing or editable:
                user_id = result['_id']
                query_user = {'_id': ObjectId(user_id)}
                loggedin_user = user_db.find_one(query_user)

                # See if item is already in wishlist. If yes, then display 'Remove from
                # wishlist' instead of 'Add to wishlist'
                inside_wl = str(tour_id) in loggedin_user['wishlist']
                # reviews_list = item['tour_reviews']

                # Retrieving the list of reviews under this listing
                # reviews_list = list(reviews_db.find({'listing': ObjectId(tour_id)}))

                # If it is 1, means display the listing. If 0 means make it invisible

                return render_template(
                    'customer/tourListing.html',
                    item=item,
                    loggedin=True,
                    user=result,
                    editable=editable,
                    # userData=tg_userData,
                    inside_wl=inside_wl,
                    display_listing=display_listing
                )

            return 'Listing is currently private'

        # if not logged in
        editable = False
        if display_listing:
            return render_template(
                'customer/tourListing.html',
                item=item,
                loggedin=False,
                editable=editable)
            # userData=tg_userData)
        return 'Listing is currently private'

    message = 'This listing is either invalid, has been hidden or deleted'
    return redirect(url_for('show_user_message', message=message))

# TOUR GUIDES
# Manage Listings: For Tour Guides to Edit/Manage their listings
@app.route('/listings')
def ownlisting():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # item = shop_db.find_one({'_id': ObjectId(tour_id)})
    # tg_id = item['tg_uid']
    # result = auth.is_auth(True)
    # userData = user_db.find_one({'_id': tg_id})

    # if not logged in
    if not result:
        return redirect(url_for('login', denied_access=True))

    # if logged in

    # Get the data of the current user
    userData = user_db.find_one({'_id': result['_id']})

    tourGuide_id = result['_id']
    tour_listings = list(shop_db.find({'tg_uid': tourGuide_id}))
    return render_template(
        'tourGuides/ownlisting.html',
        listings=tour_listings,
        loggedin=True,
        user=result,
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
    # return render_template('tourGuides/makelisting.html', form=lForm,
    # user=result)

@app.route('/listings/add', methods=['GET', 'POST'])
def makelisting():
    result = auth.is_auth(True)
    # If result is not None (User is logged in)
    if result:
        userData = user_db.find_one({'_id': ObjectId(result['_id'])})
        # Use this, don't hard code the values
        userImg = userData['profile_img']
        userName = userData['name']

        print(f'User img is: {userImg}')
        lForm = ListingForm()
        # If user submit form
        if request.method == 'POST':
            # IF all inputs are valid
            if lForm.validate_on_submit():
                tour_name = request.form['tour_name']

                detail_desc = request.form['tour_desc']

                days_form_list = request.form.getlist('tour_days_list[]')
                tour_days = formToArray(days_form_list)
                sorted_tour_days = sortDays(tour_days)

                # tour_start_time = request.form['tour_start_time']
                # tour_end_time = request.form['tour_end_time']
                # tour_time_list = [tour_start_time, tour_end_time]

                timings_form_list = request.form.getlist('tour_timings_list[]')
                tour_timings = formToArray(timings_form_list)

                itinerary_form_list = request.form.getlist('tour_items_list[]')
                tour_itinerary = formToArray(itinerary_form_list)

                locations_form_list = request.form.getlist('tour_locations_list[]')
                tour_locations = formToArray(locations_form_list)

                tour_img = request.files['tour_img']
                img_string = img_to_base64(tour_img)

                tour_revisions = request.form['tour_revisions']

                tour_price = request.form['tour_price']

                tg_uid = result['_id']

                tour_listing = Listing(
                    tour_name=tour_name,
                    tour_desc=detail_desc,
                    tour_price=tour_price,
                    tour_img=img_string,
                    tg_uid=tg_uid,
                    tour_location=tour_locations,
                    tour_revs=tour_revisions,
                    tour_itinerary=tour_itinerary,
                    tour_days=sorted_tour_days,
                    tour_time=tour_timings)

                listingInfo = tour_listing.return_obj()
                print(listingInfo)
                shop_db.insert_one(listingInfo)

                return render_template(
                    'tourGuides/listing-success.html', user=result)

            # except:
            #     tmp = list(lForm.tour_img.errors)
            #     tmp.append('File size is bigger than allowed limit of 5MB')
            #     lForm.tour_img.errors = tuple(tmp)
            #     lForm.process()
            #     return render_template(
            #         'tourGuides/makelisting.html',
            #         form=lForm,
            #         user=result)

            # IF form input is invalid
            return render_template(
                'tourGuides/makelisting.html',
                form=lForm,
                user=result)

        # This is to render the template (GET request)
        else:
            return render_template(
                'tourGuides/makelisting.html',
                form=lForm,
                user=result)

    # If not logged in
    # Return a modal where ppl have to login first
    return redirect(url_for('login', denied_access=True))

# TOUR GUIDES
# Edit Listings: When click on own listing to edit
@app.route('/listings/edit/<id>', methods=['GET', 'POST'])
def editListing(id):
    result = auth.is_auth(True)
    # If user is logged in
    if result:
        lForm = ListingForm()
        item = shop_db.find_one({'_id': ObjectId(id)})
        itinerary_list = json.dumps(item['tour_itinerary'])
        editable = item['tg_uid'] == result['_id']
        # If user is the tour_guide of this listing
        if editable:
            if request.method == 'POST':
                if lForm.validate_on_submit():
                    query_listing = {'_id': ObjectId(id)}
                    tour_name = request.form['tour_name']

                    detail_desc = request.form['tour_desc']

                    days_form_list = request.form.getlist('tour_days_list[]')
                    tour_days = formToArray(days_form_list)
                    # Remove any duplicates
                    tour_days = list(set(tour_days))
                    sorted_tour_days = sortDays(tour_days)

                    timings_form_list = request.form.getlist('tour_timings_list[]')
                    tour_timings = formToArray(timings_form_list)

                    itinerary_form_list = request.form.getlist('tour_items_list[]')
                    tour_itinerary = formToArray(itinerary_form_list)

                    locations_form_list = request.form.getlist('tour_locations_list[]')
                    tour_locations = formToArray(locations_form_list)

                    tour_revisions = request.form['tour_revisions']

                    tour_price = request.form['tour_price']

                    tg_uid = result['_id']

                    tour_img = request.files['tour_img']
                    img_string = img_to_base64(tour_img)
                    # If there's no change to image (User doesnt upload new image),
                    # keep the current image
                    print(tour_timings)

                    if img_string == '':
                        img_string = item['tour_img']
                        # Don't update the tour image
                        updated = {
                            "$set": {
                                'tour_name': tour_name,
                                'tour_desc': detail_desc,
                                'tour_price': tour_price,
                                'tour_location': tour_locations,
                                'tour_revisions': tour_revisions,
                                'tour_itinerary': tour_itinerary,
                                'tour_days': sorted_tour_days,
                                'tour_time': tour_timings
                            }}

                    else:
                        updated = {
                            "$set": {
                                'tour_name': tour_name,
                                'tour_desc': detail_desc,
                                'tour_price': tour_price,
                                'tour_img': img_string,
                                'tour_location': tour_locations,
                                'tour_revisions': tour_revisions,
                                'tour_itinerary': tour_itinerary,
                                'tour_days': sorted_tour_days,
                                'tour_time': tour_timings
                            }}

                    shop_db.update_one(query_listing, updated)

                    # Successfully updated
                    return render_template(
                        'tourGuides/editing-success.html', id=id, user=result)

                # IF form is not validated, re-render the form
                lForm.tour_desc.default = item['tour_desc']
                lForm.process()
                return render_template(
                    'tourGuides/editListing.html',
                    listing=item,
                    form=lForm,
                    user=result)

            # To render the form (GET request)
            else:
                # print(item['tour_name'])
                lForm.tour_desc.default = item['tour_desc']
                lForm.process()
                return render_template(
                    'tourGuides/editListing.html',
                    listing=item,
                    form=lForm,
                    user=result)

        # IF not allowed to edit
        else:
            message = 'You are not authorized to edit this listing!'
            return redirect(url_for('show_user_message', message=message))

    # IF the user is not logged in
    else:
        return redirect(url_for('login', denied_access=True))

# @app.route('/testImg', methods=['GET', 'POST'])
# def test_img():
#     lForm = ListingForm()
#     if request.method == 'POST':
#         tour_img = request.files['tour_img']
#         print(tour_img)
#     return render_template('tourGuides/testImg.html', form=lForm)


# TOUR GUIDES
# Hide Listings: When click on Hide button
@app.route('/listings/hide/<id>', methods=['GET', 'POST'])
def hideList(id):
    result = auth.is_auth(True)
    if result:
        item = shop_db.find_one({'_id': ObjectId(id)})
        editable = item['tg_uid'] == result['_id']

        if editable:
            query_listing = {'_id': ObjectId(id)}
            listing = shop_db.find_one(query_listing)
            updated = {
                "$set": {
                    'tour_visibility': 0,
                }}

            shop_db.update_one(query_listing, updated)
            return redirect(f'/discover/{id}')
        else:
            message = 'You are not authorized to edit this listing!'
            return redirect(url_for('show_user_message', message=message))
    return redirect(url_for('login', denied_access=True))

# TOUR GUIDES
# Show Listings: When click on show button
@app.route('/listings/show/<id>', methods=['GET', 'POST'])
def showList(id):
    result = auth.is_auth(True)
    if result:
        item = shop_db.find_one({'_id': ObjectId(id)})
        editable = item['tg_uid'] == result['_id']

        if editable:
            query_listing = {'_id': ObjectId(id)}
            listing = shop_db.find_one(query_listing)
            updated = {
                "$set": {
                    'tour_visibility': 1,
                }}

            shop_db.update_one(query_listing, updated)
            return redirect(f'/discover/{id}')
        else:
            message = 'You are not authorized to edit this listing!'
            return redirect(url_for('show_user_message', message=message))
    return redirect(url_for('login', denied_access=True))

# TOUR GUIDES
# Delete Listings: When click on Delete button
@app.route('/listings/delete/<id>', methods=['GET', 'POST'])
def deleteList(id):
    result = auth.is_auth(True)
    if result:
        item = shop_db.find_one({'_id': ObjectId(id)})
        editable = item['tg_uid'] == result['_id']
        if editable:
            # Implement validation to check if there are any exisitng tours for this listing. If there isn't, then allow it to be deleted

            # Find the list of uncompleted bookings for this listing
            uncompleted_bookings = list(bookings_db.find({'listing_id': ObjectId(id), 'completed': 0}))
            # Boolean that checks if there are uncompleted bookings
            uncompleted_exists = len(uncompleted_bookings) != 0

            # If there are no outstanding bookings, then allow listing to be deleted
            if not uncompleted_exists:
                listing = shop_db.delete_one({'_id': ObjectId(id)})
            else:
                message = 'Unable to delete listing as there are outstanding Bookings for this Listing!'
                return redirect(url_for('show_user_message', message=message))

            return redirect('/listings')
        else:
            message = 'You are not authorized to edit this listing!'
            return redirect(url_for('show_user_message', message=message))
    return redirect(url_for('login', denied_access=True))

# CUSTOMERS
# Favourites: Shows all the liked listings
@app.route('/me/favourites')
def favourites():
    # Get login status using accessor argument
    result = auth.is_auth(True)
    if result:
        user_id = result['_id']
        query_user = {'_id': ObjectId(user_id)}
        current_wishlist = user_db.find_one(query_user)['wishlist']
        current_wishlist = list(map(lambda x: ObjectId(x), current_wishlist))
        all_listings = [i for i in shop_db.find(
            {'_id': {"$in": current_wishlist}}
        )]
        print(all_listings)

        # if logged in
        return render_template(
            'customer/favourites.html',
            loggedin=True,
            user=result,
            item_list=all_listings)

    return redirect(url_for('login', denied_access=True))

# Add to wishlist
@app.route('/me/wishlist/add/<tour_id>')
def addWishlist(tour_id):
    result = auth.is_auth(True)

    if result:
        user_id = result['_id']
        query_user = {'_id': ObjectId(user_id)}
        current_wishlist = user_db.find_one(query_user)['wishlist']
        current_wishlist.append(tour_id)
        print(current_wishlist)
        updated = {
            '$set': {'wishlist': current_wishlist}
        }

        user_db.update_one(query_user, updated)

        return redirect(f'/discover/{tour_id}')

    return redirect(url_for('login', denied_access=True))

# Remove from wishlist
@app.route('/me/wishlist/remove/<tour_id>')
def removeWishlist(tour_id):
    result = auth.is_auth(True)
    if result:
        user_id = result['_id']
        query_user = {'_id': ObjectId(user_id)}
        current_wishlist = user_db.find_one(query_user)['wishlist']
        try:
            current_wishlist.remove(tour_id)
            print(current_wishlist)
            updated = {
                '$set': {'wishlist': current_wishlist}
            }

            user_db.update_one(query_user, updated)

            return redirect(f'/discover/{tour_id}')
        except:
            message = 'Unable to remove from wishlist as item does not exist in wishlist!'
            return redirect(url_for('show_user_message', message=message))
    return redirect(url_for('login', denied_access=True))

# Chat with Tour Guide
@app.route('/listings/chat/<tour_id>')
def chatwithGuide(tour_id):
    result = auth.is_auth(True)

    if result:
        browsing_user_id = result['_id']
        tour_guide_id = shop_db.find_one({'_id': ObjectId(tour_id)})['tg_uid']
        browsing_object_id = ObjectId(browsing_user_id)
        tg_object_id = ObjectId(tour_guide_id)
        # Check if there are any existing UwU chats between these 2 people
        query = {'participants': {"$in": [browsing_object_id, tg_object_id]}, 'chat_type': 'UwU'}
        chats = list(chats_db.find(query))
        # Boolean to check if a chat exists
        existing_chat = len(chats) > 0

        # Redirect to existing chat if it exists
        if existing_chat:
            existing_chat_id = chats[0]['_id']
            return redirect(url_for('chat_room', room_id=existing_chat_id))

        # If doesnt exist, create new UwU chat
        chat_id = msg.create_chat_room([browsing_user_id, tour_guide_id], False)
        return redirect(url_for('chat_room', room_id=chat_id))

    return redirect(url_for('login', denied_access=True))

# To implement dynamic calendar function
@app.route('/endpoint/bookingCalendar/<tour_id>')
def calendarUpdate(tour_id):
    print('YESH')
    try:
        day = request.args['day']
    except:
        day = None

    print(day)

    query = {'listing_id': ObjectId(tour_id), 'book_date': day}
    print(query)
    bookings = list(bookings_db.find(query, {'book_time': 1, '_id': 0}))

    # Return a list containing all the book_time of the bookings
    day_bookings = list(map(lambda x: x['book_time'], bookings))
    # Ensure there are no duplicated timings in the list
    day_bookings = list(set(day_bookings))

    print(day_bookings)

    if len(day_bookings) == 0:
        day_bookings = []

    if day:
        print('fired')
        return json.dumps({'bookedTimes': day_bookings})

    query = {}

# --------------------------------------

# Chloe

# CUSTOMER
# Your Bookings: Access all bookings
@app.route('/bookings')
def all_bookings():
    # try:
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        cust_uid = result['_id']
        booking_list = list(bookings_db.find({'cust_uid': cust_uid}))
        listings = []
        for item in booking_list:
            listings.append(shop_db.find_one({'_id': item['listing_id']}))
        booking_list.reverse()
        listings.reverse()
        return render_template(
            'customer/allBookings.html',
            booking_list=booking_list,
            listings=listings,
            loggedin=True,
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
    bchat = chats_db.find_one({'_id': booking['book_chat']})
    revisionform = RevisionForm()
    req_form = RequirementsForm()
    chat_form = msg.ChatForm()  # mbr_chat
    # Get login status using accessor argument
    result = auth.is_auth(True)
    # if not logged in
    if not result:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        if booking['process_step'] < 1:
            # Access denied, make payment first
            return redirect(url_for('checkout', book_id=book_id))
        if request.method == 'GET':
            if booking['process_step'] == 1:
                if bchat['messages']:
                    update_booking = {"$set": {"process_step": 2}}
                    bookings_db.update_one(booking, update_booking)
                    return redirect(url_for('bookings', book_id=book_id))

        chat_exist = chats_db.find({"": 101}).count() > 0
        if request.method == 'POST':
            if chat_form.validate_on_submit():
                print(
                    msg.add_message(
                        booking['book_chat'],
                        auth.get_sid(),
                        chat_form.data["message"]))
            # submit button data as a dict
            button_data = request.form.to_dict()
            if 'Submit your Requirements' in button_data.values():
                req_text = request.form["req_text"]
                update_booking = {"$set": {"process_step": 2, "customer_req": {str('requirements'): req_text}}}
                bookings_db.update_one(booking, update_booking)
                return redirect(url_for('bookings', book_id=book_id))

            elif 'AcceptItinerary' in button_data.values():
                update_booking = {"$set": {"process_step": 5}}
                bookings_db.update_one(booking, update_booking)
                return redirect(url_for('bookings', book_id=book_id))

            elif revisionform.validate_on_submit():
                revision_text = request.form["revision_text"]
                new_revisions = booking['revisions'] - 1
                if new_revisions <= 0:
                    print("paid from here on")
                update_booking = {
                    "$set": {"process_step": 4, "customer_req": {str('revision'): revision_text},
                             "revisions": new_revisions}}
                bookings_db.update_one(booking, update_booking)
                return redirect(url_for('bookings', book_id=book_id))

            elif 'CompleteTour' in button_data.values():
                update_booking = {"$set": {"process_step": 7, "completed": 1}}
                bookings_db.update_one(booking, update_booking)

                # Tour is completed, transaction
                tg_dashboard = dashboard_db.find_one({'uid': booking['tg_uid']})
                if tg_dashboard:
                    dashboard_earnings = tg_dashboard['earnings']
                    earning = booking['book_charges']['baseprice'] + \
                              booking['book_charges']['customfee']
                    dashboard_earnings.append(earning)
                    update_tg_dashboard = {'$set': {'earnings': dashboard_earnings}}
                    dashboard_db.update_one(tg_dashboard, update_tg_dashboard)
                return redirect(url_for('bookings', book_id=book_id))

        # mbr_chat
        chat_list = msg.get_chat_list_for_ui(auth.get_sid(), 'BOOKING')
        chat_room_messages = msg.get_chat_room(auth.get_sid(), booking['book_chat'])
        if not chat_room_messages:
            return redirect(url_for('chat', not_found=True))
        # mbr_chat

        return render_template('customer/booking.html',
                               process_step=booking['process_step'],
                               booking=booking,
                               tour=tour,
                               revisionform=revisionform,
                               req_form=req_form,
                               loggedin=True,
                               user=result,
                               # mbr_chat
                               chat_list=chat_list,
                               chat_form=chat_form,
                               chatroom_display=chat_room_messages["chatroom"],
                               chatroom_names=chat_room_messages["names"],
                               selected_chatroom=booking['book_chat'],
                               verification_code_OK=request.args.get('verification_code_OK'))

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

        # Do custom rendering to bookform for date and time rendering
        bookform.book_timeslot.choices = item['tour_time']

        # Dict to convert the days to numbers; for bulma-calendar options
        dayTonumber = {'Mon': 1, 'Tues': 2, 'Wed': 3, 'Thurs': 4, 'Fri': 5, 'Sat': 6, 'Sun': 0}
        listing_tour_days = item['tour_days']
        total_days = [*range(7)]
        tour_days_numbers = list(map(lambda i: dayTonumber[i], listing_tour_days))
        # Return the days that are not inside the listing days (Get the days that are not available)
        disabled_days = list(set(total_days) - set(tour_days_numbers))

        if request.method == 'POST':
            button_data = request.form.to_dict()
            if 'csrf_token' in button_data:
                book_date = request.form["book_day"]
                book_time = request.form["book_timeslot"]

                tg_booking_list = list(bookings_db.find({'tg_uid': item['tg_uid']}))
                if bookform.date_valid(book_date, tg_booking_list) and bookform.time_valid(book_time):
                    chat_id = msg.create_chat_room([result['_id'], item["tg_uid"]], True)
                    booking = Booking(
                        tg_uid=item['tg_uid'],
                        cust_uid=result['_id'],
                        listing_id=item['_id'],
                        book_date=book_date,
                        book_time=book_time,
                        book_baseprice=item['tour_price'],
                        book_customfee=0,
                        book_duration="",
                        timeline_content=item['tour_itinerary'],
                        chat_id=chat_id,
                        revisions=int(item['tour_revisions']),
                        process_step=float(5))
                    inserted_booking = bookings_db.insert_one(booking.return_obj())
                    book_id = inserted_booking.inserted_id
                    return redirect(url_for('checkout', book_id=book_id))

            elif 'CustomiseTour' in button_data.values():
                customfee = round(0.1 * float(item['tour_price']), 2)
                chat_id = msg.create_chat_room([result['_id'], item["tg_uid"]], True)
                booking = Booking(
                    tg_uid=item['tg_uid'],
                    cust_uid=result['_id'],
                    listing_id=item['_id'],
                    book_date='',
                    book_time='',
                    book_baseprice=item['tour_price'],
                    book_customfee=customfee,
                    book_duration="",
                    timeline_content=item['tour_itinerary'],
                    chat_id=chat_id,
                    revisions=int(item['tour_revisions']),
                    process_step=float(0))
                inserted_booking = bookings_db.insert_one(booking.return_obj())
                book_id = inserted_booking.inserted_id
                return redirect(url_for('checkout', book_id=book_id))

            elif 'ChatFirst' in button_data.values():
                chat_list = list(
                    chats_db.find({'participants': {"$in": [auth.get_sid(), item["tg_uid"]]}, 'chat_type': 'UwU'}))
                if len(chat_list) > 0:
                    chat_id = chat_list[0]['_id']
                    return redirect(url_for('chat_room', room_id=chat_id))
                else:
                    chat_id = msg.create_chat_room([result['_id'], item["tg_uid"]], False)
                    return redirect(url_for('chat_room', room_id=chat_id))

        return render_template(
            'customer/book-now.html',
            loggedin=True,
            user=result,
            bookform=bookform,
            item=item,
            tour_id=tour_id,
            disabled_days=disabled_days)
    # if not logged in
    else:
        return redirect(url_for('login', denied_access=True))

# except:
#     return 'Error trying to render'


# CUSTOMER
# Checkout page (placeholder)
@app.route('/checkout/<book_id>', methods=['GET', 'POST'])
def checkout(book_id):
    # try:
    booking = bookings_db.find_one({'_id': ObjectId(book_id)})
    tour = shop_db.find_one({'_id': ObjectId(booking['listing_id'])})
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
                    # Transaction
                    earnings = booking['book_charges']['baseprice'] + \
                               booking['book_charges']['customfee']
                    transaction = Transaction(
                        tg_uid=booking['tg_uid'],
                        cust_uid=booking['cust_uid'],
                        earnings=earnings,
                        booking=booking['_id'],
                        tour_name=tour['tour_name'])
                    transaction.payment_made()
                    transaction_db.insert_one(transaction.return_obj())

                    return redirect(url_for('bookings', book_id=str(book_id)))
                elif booking['process_step'] == 0:
                    update_booking = {"$set": {"process_step": 1}}
                    bookings_db.update_one(booking, update_booking)
                    return redirect(url_for('bookings', book_id=str(book_id)))

                else:
                    print("Error occurred while trying to pay.")

        return render_template(
            'customer/checkout.html',
            loggedin=True,
            user=result,
            booking=booking,
            form=form,
            book_id=book_id)
    # if not logged in
    else:
        return redirect(url_for('login', denied_access=True))

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
            return redirect(url_for('login', denied_access=True))
        # if logged in
        else:
            tg_uid = result['_id']
            booking_list = list(bookings_db.find({'tg_uid': tg_uid}))
            listings = []
            # [for i in bookings_db.find(
            #     {'tg_uid': tg_uid})]

            for item in booking_list:
                listings.append(shop_db.find_one({'_id': item['listing_id']}))
            booking_list.reverse()
            listings.reverse()
            return render_template(
                'tourGuides/allBusinesses.html',
                booking_list=booking_list,
                listings=listings,
                loggedin=True,
                user=result)
    except BaseException:
        return 'Error trying to render'

# TOUR GUIDES
# Individual gigs
# @app.route('/s/businesses/<id>')
@app.route('/s/businesses/<book_id>', methods=['GET', 'POST'])
def business(book_id):
    booking_query = {'_id': ObjectId(book_id)}
    booking = bookings_db.find_one(booking_query)
    listing = shop_db.find_one({'_id': booking['listing_id']})
    bchat = chats_db.find_one({'_id': booking['book_chat']})
    # Get login status using accessor argument
    result = auth.is_auth(True)
    AddInfo_form = AddInfoForm()
    itineraryForm = EditPlan()
    chat_form = msg.ChatForm()  # mbr_chat
    # if not logged in
    if not result:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        if booking['process_step'] < 1:
            # access denied, customer has yet to pay
            return redirect(url_for('all_businesses'))
        chat_exist = chats_db.find({"": 101}).count() > 0
        if request.method == "POST":
            data_dict = request.form.to_dict()
            if itineraryForm.is_submitted() and 'Update Itinerary' in data_dict.values():
                tour_date = request.form["tour_date"]
                tour_date = datetime.strptime(tour_date, '%Y-%m-%d').strftime('%m/%d/%y')

                tour_starttime = request.form["tour_starttime"]
                tour_endtime = request.form["tour_endtime"]
                format_starttime = datetime.strptime(tour_starttime, "%H:%M")
                format_endtime = datetime.strptime(tour_endtime, "%H:%M")
                tour_time = str(format_starttime.strftime("%I:%M %p") + " - " + format_endtime.strftime("%I:%M %p"))

                tour_price = float(request.form["tour_price"])

                itinerary_form_list = request.form.getlist('tour_items_list[]')
                tour_itinerary = formToArray(itinerary_form_list)
                updated = {
                    "$set": {"timeline_content": tour_itinerary,
                             "book_date": tour_date,
                             "book_time": tour_time,
                             "book_charges.baseprice": tour_price,
                             "process_step": 3}
                }
                bookings_db.update_one(booking_query, updated)
                return redirect(url_for('business', book_id=book_id))

            if AddInfo_form.validate_on_submit():
                AddInfo = request.form['AddInfo']
                updated = {
                    "$set": {"book_info": AddInfo}
                }
                bookings_db.update_one(booking, updated)
            elif chat_form.validate_on_submit():
                # print(chat_form.data["message"])
                print(
                    msg.add_message(
                        booking['book_chat'],
                        auth.get_sid(),
                        chat_form.data["message"]))

        # mbr_chat
        chat_list = msg.get_chat_list_for_ui(auth.get_sid(), 'BOOKING')
        chat_room_messages = msg.get_chat_room(auth.get_sid(), booking['book_chat'])
        if not chat_room_messages:
            return redirect(url_for('chat', not_found=True))
        # mbr_chat

        return render_template('tourGuides/business.html',
                               process_step=booking['process_step'],
                               booking=booking,
                               listing=listing,
                               loggedin=True,
                               user=result,
                               form=itineraryForm,
                               addInfoForm=AddInfo_form,
                               # mbr_chat
                               chat_list=chat_list,
                               chat_form=chat_form,
                               chatroom_display=chat_room_messages["chatroom"],
                               chatroom_names=chat_room_messages["names"],
                               selected_chatroom=booking['book_chat'],
                               verification_code_OK=request.args.get('verification_code_OK'))
    # except BaseException:
    #     return 'Error trying to render'

# CUSTOMER
# Submit Review
@app.route('/review/<book_id>', methods=['GET', 'POST'])
def review(book_id):
    # try:
    transaction = transaction_db.find_one({'booking': ObjectId(book_id)})
    booking = list(bookings_db.find({'_id': ObjectId(book_id)}))[0]
    listing_id = booking['listing_id']
    tour = list(shop_db.find({'_id': ObjectId(listing_id)}))
    customer = list(user_db.find({'_id': booking['cust_uid']}))

    form = ReviewForm()
    result = auth.is_auth(True)
    if not result:
        return redirect(url_for('login', denied_access=True))
    else:
        # if reviewer is customer/tg
        if result['_id'] == booking['cust_uid']:
            # Customer is the reviewer, reviewing the tour/ tour guide
            review_type = "tour"
            reviewee_id = booking['tg_uid']

            # query = {'tour_reviews': {"$in": [ObjectId(book_id)]}, '_id':ObjectId(booking[0]['listing_id'])}

            # A list of all the booking IDs of the reviews for this listing
            tmp1 = list(map(lambda i: i['tour_reviews'], tour))[0]
            listing_review_bookingIDs = list(map(lambda i: i['booking'], tmp1))
            review_exists = ObjectId(book_id) in listing_review_bookingIDs

        elif result['_id'] == booking['tg_uid']:
            # TG is the reviewer, reviewing the customer
            review_type = "customer"
            reviewee_id = booking['cust_uid']

            # tmp1 = list(map(lambda i: i['user_reviews'], customer))[0]
            # print(tmp1)
            # user_review_bookingIDs = list(map(lambda i: i['booking'], tmp1))
            # review_exists = ObjectId(book_id) in user_review_bookingIDs
            # print(review_exists)
            review_exists = False

        # If this review already exists
        if review_exists:
            return redirect(url_for('bookings', book_id=book_id))
        elif booking['process_step'] < 7:
            print("access denied, go on tour first")
            return redirect(url_for('bookings', book_id=book_id))
        else:
            if request.method == "POST":
                if form.is_submitted():
                    review = Review(
                        stars=int(form.rating.data),
                        text=request.form["review_text"],
                        reviewer_id=result['_id'],
                        reviewee_id=reviewee_id,
                        booking=booking['_id'],
                        listing=tour[0]['_id'])

                    review_data = review.return_obj()
                    if review_type == "tour":
                        # Update the Listing db, append the review to 'Reviews'
                        listing_query = {'_id': ObjectId(booking['listing_id'])}
                        updated = {'$push': {'tour_reviews': review_data}}
                        shop_db.update_one(listing_query, updated)

                        update_transaction = {"$set": {'rating': int(form.rating.data)}}
                        transaction_db.update_one(transaction, update_transaction)
                    elif review_type == "customer":
                        query = {'_id': ObjectId(booking['cust_uid'])}
                        updated = {'$push': {'user_reviews': review_data}}
                        user_db.update_one(query, updated)

                    # reviews_db.insert_one(review.return_obj())

                    if booking['process_step'] == 7.1 or booking['process_step'] == 7.2:
                        # The other party has left a review already
                        new_step = 8
                    elif booking['process_step'] == 7:
                        if review_type == 'tour':
                            new_step = 7.1
                        elif review_type == 'customer':
                            new_step = 7.2
                    update_booking = {"$set": {'process_step': new_step}}
                    bookings_db.update_one(booking, update_booking)
                    return redirect(url_for('bookings', book_id=book_id))

            return render_template(
                'customer/review.html',
                booking=booking,
                tour=tour[0],
                form=form,
                review_type=review_type)

# except BaseException:
#     return 'Error trying to render'

# --------------------------------------

# Dylan

# TOUR GUIDE
# Redirect user to dashboard if attempt to access root of /s/


@app.route('/tg/')
def sellerModeDir():
    return redirect(url_for('sellerDashboard'))

# Redirect user to dashboard if attempt to access file of /s/
@app.route('/tg')
def sellerModeFile():
    return redirect(url_for('sellerDashboard'))

# TOUR GUIDE
# Dashboard
@app.route('/tg/dashboard', methods=['POST', 'GET'])
def sellerDashboard():
    # Get login status using accessor argument
    result = auth.is_auth(True)

    # Declare WTForm
    form = dashboard.ReportGenForm()

    # if not logged in
    if not result:
        return redirect(url_for('login', denied_access=True))
    # if logged in
    else:
        if form.validate_on_submit():
            # Get data from form
            date_scope = form.data['date_filter']

            # Parse data into machine readable format
            date_split = date_scope.split("-")

            if date_scope == "":
                report_name = dashboard.generate_report(auth.get_user_id(auth.get_sid()))
            else:
                report_name = dashboard.generate_report(auth.get_user_id(auth.get_sid()), date_split[0], date_split[1])

            # Threading function to delete file if left undownloaded
            def delete_after_generate():
                # do something that takes a long time
                import time

                # Check after 10 seconds after report generation for file existence
                time.sleep(20)

                # File doesn't exist due to deletion by reports(), exit thread
                if not os.path.exists(f"./tmp_data/{report_name}"):
                    return

                # Delay delete for 60 seconds to ensure file has been successfully fetched by client
                time.sleep(60)

                # Try to delete file again
                os.remove(f"./tmp_data/{report_name}")

            # Start process to delete file
            thread = Thread(target=delete_after_generate)
            thread.start()

            # Change date_scope value for cosmetic purposes
            if date_scope == "":
                date_scope = "ALL"

            return redirect(
                url_for('reports', filename=f"{report_name}.xlsx", name=result["name"], date_scope=date_scope))

        earnings_breakdown_data = dashboard.get_earning_breakdown(result['_id'])
        satisfaction_breakdown_data = dashboard.get_satisfaction_rate(result['_id'])
        earning_average_tour = dashboard.get_avg_per_tour(result['_id'])

        # print(satisfaction_breakdown_data)

        return render_template(
            'tourGuides/dashboard.html',
            loggedin=True,
            user=result,
            form=form,
            earning_data=earnings_breakdown_data,
            csat_data=satisfaction_breakdown_data,
            avg_per_tour=earning_average_tour
        )

@app.route('/s/report/<filename>')
def reports(filename):
    def delete_after_download():
        # do something that takes a long time
        import time
        # Delay delete for 5 seconds to ensure file has been successfully fetched by client
        time.sleep(5)
        os.remove(f"./tmp_data/{filename}")

    user_obj = auth.is_auth(True)

    if not user_obj:
        return redirect(url_for('login', denied_access=True))

    if not os.path.exists(f"./tmp_data/{filename}"):
        print("not found")
        return abort(404)

    # Delete file after 5 seconds when download has started.
    thread = Thread(target=delete_after_download)
    thread.start()

    # Send report to client
    return send_from_directory(os.path.join('.', 'tmp_data'), filename,
                               as_attachment=True,
                               attachment_filename=
                               f'TourisitReport-{request.args.get("name")}-{request.args.get("date_scope")}.xlsx')

# INTERNAL
# Admin Dashboard -- Private internal shit
# @app.route('/admin')
# def adminDashboard():
#     # Get login status using accessor argument
#     result = auth.is_auth(True)
#     # if not logged in
#     if not result or result['account_type'] != 1:
#         return redirect(url_for('login', denied_access=True))
#     # if logged in
#     else:
#         return render_template(
#             'internal/dashboard.html',
#             loggedin=True,
#             user=result)


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
        return render_template(
            'internal/users.html',
            loggedin=True,
            user=result,
            user_list=user_accounts)

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
        return render_template(
            'internal/listings.html',
            loggedin=True,
            user=result,
            listing=admin.list_listings())

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
                return render_template(
                    'auth/login.html', form=form, acc_login_failed=True)
            elif result == "UNVERIFIED":
                return redirect(
                    url_for(
                        'signup',
                        unverified_email_ref=True,
                        email=email))
            else:
                # If pass, set cookie and redirect
                resp = redirect(url_for('home'))
                resp.set_cookie('tourisitapp-sid', result)
                # resp.set_cookie('tourisitapp-uid', auth.get_user_id(result))
                return resp

        # If GET request // Show page
        return render_template(
            'auth/login.html',
            form=form,
            denied_access=request.args.get('denied_access'),
            verification_code_OK=request.args.get('verification_code_OK'),
            verification_code_denied=request.args.get('verification_code_denied'))
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

    # Check was this a ref from login because user hasn't gotten their email
    # verified.
    if request.args.get('unverified_email_ref') == "True" and request.args.get(
            'email') is not None:
        return render_template(
            'auth/signup.html',
            signupform=signup_form,
            resend_email=resend_email_form,
            acc_creation=True,
            email=request.args.get('email'))

    # If user is NOT logged in
    if not auth.is_auth():
        # Do if POST response // Form submission
        if signup_form.validate_on_submit():
            name = signup_form.data['full_name']
            email = signup_form.data['email']
            password = signup_form.data['password']

            # create_account implements auth
            if auth.create_account(name, password, email):
                return render_template(
                    'auth/signup.html',
                    signupform=signup_form,
                    resend_email=resend_email_form,
                    acc_creation=True,
                    email=email)
            else:
                return render_template(
                    'auth/signup.html',
                    signupform=signup_form,
                    exist=True,
                    email=email)

        # If GET request // Show page
        return render_template(
            'auth/signup.html',
            signupform=signup_form,
            resend_email=resend_email_form,
            newEmailSent=request.args.get('email_sent'))
    # If user is ALREADY logged in
    else:
        return redirect(url_for('home'))

@app.route('/endpoint/resendEmail', methods=['POST'])
def resend_email():
    resend_email_form = auth.ResendEmailForm()
    # if resend_email_form.validate_on_submit():
    email = resend_email_form.data["email"]

    # print(email)

    # if auth.get_sid() is not None:
    #     sid = auth.get_sid()
    #     if auth.send_confirmation_email(sid, None):
    #         print("Email sent via SID")
    #         return redirect(url_for('signup', email_sent=True))

    if email is not None:
        if auth.send_confirmation_email("email_verification", email):
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
        chat_list = msg.get_chat_list_for_ui(auth.get_sid(), 'UwU')
        return render_template(
            'chat.html',
            loggedin=True,
            user=result,
            list=chat_list,
            chatroom_display=False,
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
            print(
                msg.add_message(
                    room_id,
                    auth.get_sid(),
                    chat_form.data["message"]))

        chat_list = msg.get_chat_list_for_ui(auth.get_sid(), 'UwU')
        chat_room_messages = msg.get_chat_room(auth.get_sid(), room_id)

        if not chat_room_messages:
            return redirect(url_for('chat', not_found=True))

        return render_template(
            'chat.html',
            loggedin=True,
            user=result,
            list=chat_list,
            form=chat_form,
            chatroom_display=chat_room_messages["chatroom"],
            chatroom_names=chat_room_messages["names"],
            selected_chatroom=ObjectId(room_id),
            verification_code_OK=request.args.get('verification_code_OK'))

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
                shard_payload = render_template(
                    'components/shards/msg.html',
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

@app.route('/set_acc_mode', methods=['GET', 'POST'])
def setAccType():
    result = auth.is_auth(True)
    if result:
        sForm = auth.SelectAccModeForm()
        if request.method == 'POST':
            acc_mode = int(request.form['acc_mode'])
            print(acc_mode)
            query = {'_id': ObjectId(result['_id'])}
            updated = {
                "$set": {
                    'account_mode': acc_mode}
            }

            user_db.update_one(query, updated)

            return redirect(url_for('home'))

        return render_template('onboarding/confirmaccType.html', setAccModeForm=sForm, loggedin=True, user=result)

    message = 'Not authorized to perform this action!'
    return redirect(url_for('show_user_message', message=message))

# Password reset:
# TODO: Take token put into WTForm and check only after submission. Remove check on auth.py
# @app.route('/login/reset_password')
# def email_confirmation_endpoint():
#     email_token = request.args.get('token')
#     if auth.verify_remove_token("email_verification", email_token):
#         return redirect(url_for('login', verification_code_OK=True))
#     else:
#         return redirect(url_for('login', verification_code_denied=True))


# ALL ERROR HANDLING IS HERE
@app.errorhandler(413)
def error413(err):
    return f'Oh Noes! You got {err}'

# Run app
if __name__ == '__main__':
    app.run(debug=True, threaded=True)

# Use this if running on server
# if __name__ == '__main__':
#     app.run(debug=True, threaded=True, host='0.0.0.0')
