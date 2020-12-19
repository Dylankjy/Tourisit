import models.Validation as validation

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