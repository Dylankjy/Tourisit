from routes import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class User(db.Model):
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
    guide_id = db.Column(db.String(30), ForeignKey='users.user_id')
    tours = db.Column(db.String(30), nullable=False)


class Listing(db.Model, User):
    __tablename__ = 'listings'
    tour_id = db.Column(db.Integer, primary_key=True)
    tour_name = db.Column(db.String(30), nullable=False, unique=True)
    tour_brief = db.Column(db.String(50), nullable=False)
    tour_desc = db.Column(db.String(300), nullable=False)
    tour_price = db.Column(db.Integer, nullable=False)
    tour_img = db.Column(db.String(10), nullable=False, unique=True)
    tour_guide = db.Column(db.String(30), db.ForeignKey('tourguides.guide_id'))
    date_created = db.Column(db.DateTime, default=datetime.now)

