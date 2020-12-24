import models.Validation as validation

from datetime import datetime


class Listing:
    def __init__(
        self,
        tour_name,
        tour_brief,
        tour_price,
        tg_uid,
        tour_img=''
    ):

        self.__tour_name = ''
        self.set_tour_name(tour_name)

        self.__tour_brief = ''
        self.set_tour_brief(tour_brief)

        self.__tour_img = ''
        self.set_tour_img(tour_img)

        self.__tour_itinerary = []
        self.__tour_location = []
        self.__tour_price = tour_price

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
            assert len(tour_brief) <= 200
        except AssertionError:
            print(f"{tour_brief} must be less than {200} characters!")
        else:
            self.__tour_brief = tour_brief

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
            "tour_itinerary": self.__tour_itinerary,
            "tour_location": self.__tour_location,
            "tour_price": self.__tour_price,
            "tour_img": self.__tour_img,
            "date_created": self.__date_created,
            "tour_rating": self.__tour_rating,
            "tour_review": self.__tour_review,
            "tg_uid": self.__tg_uid,
        }