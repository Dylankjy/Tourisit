from routes import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class User():
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    user_name = db.Column(db.String(30), nullable=False, unique=True)
    user_password = db.Column(db.String(30), nullable=False)
    user_rating = db.Column(db.String(30), nullable=False)
    user_img = db.Column(db.String(30))


class Customer(db.Model, User):
    __tablename__ = 'cutomers'
    wishlist = db.Column(db.String(30), nullable=False, unique=True)


class TourGuides(db.Model, User):
    __tablename__ = 'tourguides'
    #Creates an artificial column in 'Listing' table called 'tour_guide'.
    # TourGuides['tours'] = Listing
    # Listing['tour_guide'] = TourGuides
    tours = db.relationship('Listing', backref='tour_guide')


class Listing(db.Model):
    __tablename__ = 'listings'
    tour_id = db.Column(db.Integer, primary_key=True)
    tour_name = db.Column(db.String(30), nullable=False, unique=True)
    tour_brief = db.Column(db.String(50), nullable=False)
    tour_desc = db.Column(db.String(300), nullable=False)
    tour_price = db.Column(db.Integer, nullable=False)
    tour_img = db.Column(db.String(10), unique=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
