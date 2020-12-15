from datetime import datetime


class User:
    def __init__(
        self,
        name,
        password,
        email,
        phone_number,
        bio,
        profile_img,
        last_seen,
        last_activity,
        stripe_ID,
        wishlist,
        fb,
        insta,
        linkedin,
    ):
        self.__name = name
        self.__password = password
        self.__email = email
        self.__phone_number = phone_number
        self.__bio = bio
        self.__profile_img = profile_img
        self.__last_seen = last_seen
        self.__last_activity = last_activity
        self.__stripe_ID = stripe_ID
        self.__wishlist = wishlist
        self.__fb = fb
        self.__insta = insta
        self.__linkedin = linkedin

    def return_obj(self):
        return {
            "name": self.__name,
            "password": self.__password,
            "email": self.__email,
            "phone_number": self.__phone_number,
            "bio": self.__bio,
            "profile_img": self.__profile_img,
            "last_seen": self.__last_seen,
            "last_activity": self.__last_activity,
            "stripe_id": self.__stripe_ID,
            "wishlist": self.__wishlist,
            "socialmedia": {
                "fb": self.__fb,
                "insta": self.__insta,
                "linkedin": self.__linkedin,
            },
        }


def validate_len(name, leng):
    try:
        assert len(name) <= leng
    except AssertionError:
        print(f"{name} must be less than {leng} characters!")
    else:
        return name


def validate_type(name, dtype):
    try:
        assert type(name) == dtype
    except AssertionError:
        print(f"{name} must be of type {dtype}")
    else:
        return dtype


class Listing:
    def __init__(
        self,
        tour_name,
        tour_brief,
        tour_itinerary,
        tour_location,
        tour_price,
        date_created,
        tg_uid,
        tour_img="",
    ):
        self.__tour_name = tour_name
        self.__tour_brief = tour_brief
        self.__tour_itinerary = tour_itinerary
        self.__tour_location = tour_location
        self.__tour_price = tour_price
        self.__tour_img = bytes("")
        self.__date_created = datetime.now()
        self.__tour_rating = 0
        self.__tour_review = []
        self.__tguid = tg_uid

    def set_tour_name(self, tour_name):
        tour_name = validate_len(tour_name, 30)
        self.__tour_name = tour_name

    def set_tour_brief(self, tour_brief):
        tour_brief = validate_len(tour_brief, 200)
        self.__tour_brief = tour_brief

    def add_tour_itinerary(self, itinerary):
        itinerary = validate_type(itinerary, str)
        self.__tour_review.append(itinerary)

    def set_tour_location(self, tour_location):
        tour_location = validate_type(tour_location, list)
        self.__tour_location = tour_location

    def set_tour_price(self, tour_price):
        tour_price = validate_type(tour_price, float)
        self.__tour_price = tour_price

    def set_tour_img(self, tour_img):
        tour_img = validate_type(tour_img, bytes)
        self.__tour_img = tour_img

    def set_tour_rating(self, tour_rating):
        tour_rating = validate_type(tour_rating, float)
        try:
            assert tour_rating <= 5
        except AssertionError:
            print("Tour Rating must be less than or equal to 5!")
        else:
            self.__tour_rating = tour_rating

    def set_tour_review(self, tour_review):
        tour_review = validate_type(tour_review, list)
        self.__tour_review = tour_review

    def set_tguid(self, tguid):
        self.__tguid = tguid

    def return_obj(self):
        return {
            "tour_name": self.__tour_name,
            "tour_brief": self.__tour_brief,
            "tour_itinerary": self.__tour_itinerary,
            "tour_location": self.__tour_location,
            "tour_price": self.__tour_price,
            "tour_img": self.__tour_img,
            "date_created": self.__date_created,
            "tour_rating": self.__tour_rating,
            "tour_review": self.__tour_review,
            "tg_uid": self.__tg_uid,
        }


class Bookings:
    def __init__(
        self,
        tg_uid,
        cust_uid,
        listing,
        chat,
        datetime,
        duration,
        info,
        timeline_content,
        process_step,
    ):
        self.__tg_uid = tg_uid
        self.__cust_uid = cust_uid
        self.__listing = listing
        self.__chat = chat
        self.__datetime = datetime
        self.__duration = duration
        self.__info = info
        self.__timeline_content = timeline_content
        self.__process_step = process_step

    def return_obj(self):
        return {
            "tg_uid": self.__tg_uid,
            "cust_uid": self.__cust_uid,
            "listing": self.__listing,
            "chat": self.__chat,
            "datetime": self.__datetime,
            "duration": self.__duration,
            "info": self.__info,
            "timeline_content": self.__timeline_content,
            "process_step": self.__process_step,
        }


class Transactions:
    def __init__(self, tg_uid, cust_uid, pay_id, cost, booking):
        self.__tg_uid = tg_uid
        self.__cust_uid = cust_uid
        self.__pay_id = pay_id
        self.__cost = cost
        self.__booking = booking

    def return_obj(self):
        return {
            "tg_uid": self.__tg_uid,
            "cust_uid": self.__cust_uid,
            "pay_id": self.__pay_id,
            "cost": self.__cost,
            "booking": self.__booking,
        }


class Chat:
    def __init__(self, sender_id, receiver_id, msg_content):
        self.__sender_id = sender_id
        self.__receiver_id = receiver_id
        self.__msg_content = msg_content

    def return_obj(self):
        return {
            "sender_id": self.__sender_id,
            "receiver_id": self.__receiver_id,
            "msg_content": self.__msg_content,
        }


class Review:
    def __init__(self, stars, text, reviewer_id, reviewee_id):
        self.__stars = stars
        self.__text = text
        self.__reviewer_id = reviewer_id
        self.__reviewee_id = reviewee_id

    def return_obj(self):
        return {
            "stars": self.__stars,
            "text": self.__text,
            "reviewer": self.__reviewer_id,
            "reviewee": self.__reviewee_id,
        }


class Support:
    def __init__(self, uid, support_type, content, status):
        self.__uid = uid
        self.__support_type = support_type
        self.__content = content
        self.__status = status

    def return_obj(self):
        return {
            "uid": self.__uid,
            "support_type": self.__support_type,
            "content": self.__content,
            "status": self.__status,
        }