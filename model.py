# from routes import db
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    user_password = db.Column(db.String(30), nullable=False)
    user_rating = db.Column(db.String(30), nullable=False)
    user_img = db.Column(db.String(30))

    #Customer
    wishlist = db.Column(db.String(30))

    #Tour Guide
    # Creates an artificial column in 'Listing' table called 'tour_guide'.
    # COMMENT OUT THE NEXT 3 LINES!
    # TourGuides['tours'] = Listing
    # Listing['tour_guide'] = TourGuides
    # backref='tour_guide' means you can do Listing(tour_guide=jake) where jake is a TourGuide Object
    tours = db.relationship('Listing', backref='tour_guide')


# class Customers(db.Model, User):
#     __tablename__ = 'customers'
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
#     wishlist = db.Column(db.String(30), nullable=False, unique=True)


# class TourGuides(db.Model, User):
#     __tablename__ = 'tourguides'
#     user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
#     #Creates an artificial column in 'Listing' table called 'tour_guide'.
#     # COMMENT OUT THE NEXT 3 LINES!
#     # TourGuides['tours'] = Listing
#     # Listing['tour_guide'] = TourGuides
#     # backref='tour_guide' means you can do Listing(tour_guide=jake) where jake is a TourGuide Object
#     tours = db.relationship('Listing', backref='tour_guide')


class Listing(db.Model):
    __tablename__ = 'listings'
    tour_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    tour_name = db.Column(db.String(30), nullable=False, unique=True)
    tour_brief = db.Column(db.String(50), nullable=False)
    tour_desc = db.Column(db.String(500), nullable=False)
    tour_price = db.Column(db.Integer, nullable=False)
    tour_img = db.Column(db.String(10), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now)

    #You need to hav ea common column beteen Listing and Users in order to join them
    tour_guide_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
