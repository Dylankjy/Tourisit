from datetime import datetime

class User():
    def __init__(self, name, password, email, phone_number, bio, profile_img, last_seen, last_activity, stripe_ID, wishlist):
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

    def return_obj(self):
        return {'name': self.__name, 'password': self.__password, 'email': self.__email, 'phone_number': self.__password, 'bio': self.__bio, 
        'profile_img': self.__profile_img, 'last_seen': self.__profile_img, 'last_activity': self.__last_activity, 'stripe_id': self.__stripe_ID, "wishlist": self.__wishlist}


def validate_len(name, leng):
    try:
        assert len(name) <= leng
    except AssertionError:
        print(f'{name} must be less than {leng} characters!')
    else:
        return name


def validate_type(name, dtype):
    try:
        assert type(name) == dtype
    except AssertionError:
        print(f'{name} must be of type {dtype}')
    else:
        return dtype


class Listing():
    def __init__(self, tour_name, tour_brief, tour_itinerary, tour_location, tour_price, date_created, tg_uid, tour_img=''):
        self.__tour_name = tour_name
        self.__tour_brief = tour_brief
        self.__tour_itinerary = tour_itinerary
        self.__tour_location = tour_location
        self.__tour_price = tour_price
        self.__tour_img = bytes('')
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
            print('Tour Rating must be less than or equal to 5!')
        else:
            self.__tour_rating = tour_rating

    def set_tour_review(self, tour_review):
        tour_review = validate_type(tour_review, list)
        self.__tour_review = tour_review

    def set_tguid(self, tguid):
        self.__tguid = tguid


    def return_obj(self):
        return {"tour_name": self.__tour_name, "tour_brief": self.__tour_brief, "tour_itinerary": self.__tour_itinerary, "tour_price": self.__tour_price,
                "tour_img": self.__tour_img, "date_created": self.__date_created, "tour_rating": self.__tour_rating, "tour_review":self.__tour_rating, "tg_uid":tg_uid}

        
class Bookings():
    def __init__(self, chat, datetime, duration, info, timeline_content, process_step):
        self.__chat = chat
        self.__datetime = datetime
        self.__duration = duration
        self.__info = info
        self.__timeline_content = timeline_content
        self.__process_step = process_step
        

class Transactions():
    def __init__(self, pid, cost, listing):
        self.__pid = pid
        self.__cost = cost
        self.__listing = listing
        

class Support():
    def __init__(self, uid, support_type, content, status):
        self.__uid = uid
        self.__support_type = support_type
        self.__content = content
        self.__status = status
    
    def return_obj(self):
        return {'uid': self.__uid, 'support_type': self.__support_type, 'content': self.__support_type, 'status': self.__status}


