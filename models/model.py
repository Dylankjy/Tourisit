from datetime import datetime
import models.Validation as validation


class Booking:
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


class Listing:
    def __init__(
        self,
        tour_name,
        tour_brief,
        tour_desc,
        tour_price,
        tg_uid,
        tour_img=''
    ):

        self.__tour_name = ''
        self.set_tour_name(tour_name)

        self.__tour_brief = ''
        self.set_tour_brief(tour_brief)

        self.__tour_desc = ''
        self.set_tour_desc(tour_desc)

        self.__tour_itinerary = []
        self.__tour_location = []
        self.__tour_price = 0
        self.set_tour_price(tour_price)

        self.__tour_img = ''
        self.set_tour_img(tour_img)

        self.__date_created = datetime.now()
        self.__tour_rating = 0
        self.__tour_review = []
        self.set_tg_uid(tg_uid)

    def set_tour_name(self, tour_name):
        try:
            assert len(tour_name) <= 30
        except AssertionError:
            print(f"{tour_name} must be less than {30} characters!")
        else:
            self.__tour_name = tour_name

    def set_tour_brief(self, tour_brief):
        try:
            assert len(tour_brief) <= 100
        except AssertionError:
            print(f"Brief Tour Description must be less than 100 characters!")
        else:
            self.__tour_brief = tour_brief

    def set_tour_desc(self, tour_desc):
        self.__tour_desc = tour_desc

    def add_tour_itinerary(self, itinerary):
        try:
            assert type(itinerary) == str
        except AssertionError:
            print(f"{itinerary} must be of type {str}")
        else:
            self.__tour_review.append(itinerary)

    def set_tour_location(self, tour_location):
        try:
            assert type(tour_location) == list
        except AssertionError:
            print(f"{tour_location} must be of type {list}")
        else:
            self.__tour_location.append(tour_location)

    def set_tour_price(self, tour_price):
        try:
            tour_price = float(tour_price)
        except ValueError:
            print(f"{tour_price} must be of type {float}")
        else:
            self.__tour_price = tour_price

    def set_tour_img(self, tour_img):
        try:
            assert type(tour_img) == bytes
        except AssertionError:
            print(f"{tour_img} must be of type {bytes}")
        else:
            self.__tour_img = tour_img

    def set_tour_rating(self, tour_rating):
        try:
            tour_rating = float(tour_rating)
        except ValueError:
            print(f"{tour_rating} must be of type {float}")
        else:
            self.__tour_rating = tour_rating

    def set_tour_review(self, tour_review):
        try:
            assert type(tour_review) == list
        except AssertionError:
            print(f"{tour_review} must be of type {list}")
        else:
            self.__tour_review.append(tour_review)

    def set_tg_uid(self, tg_uid):
        self.__tg_uid = tg_uid

    def return_obj(self):
        return {
            "tour_name": self.__tour_name,
            "tour_brief": self.__tour_brief,
            "tour_desc": self.__tour_desc,
            "tour_itinerary": self.__tour_itinerary,
            "tour_location": self.__tour_location,
            "tour_price": self.__tour_price,
            "tour_img": self.__tour_img,
            "date_created": self.__date_created,
            "tour_rating": self.__tour_rating,
            "tour_review": self.__tour_review,
            "tg_uid": self.__tg_uid,
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


class User:
    def __init__(
        self,
        name,
        password,
        email,
        phone_number='',
        bio='',
        profile_img='',
        last_seen='',
        last_activity='',
        stripe_ID='',
        wishlist=[],
        fb='',
        insta='',
        linkedin='',
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


class Transaction:
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

