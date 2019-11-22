# import os
import json
# import sqlite3

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


association_table = db.Table('association', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable = False)
    year = db.Column(db.String, nullable = False)
    bio = db.Column(db.String, nullable = False)
    looking_for_buddy = db.Column(db.String, nullable = False)  
    events_owned = db.Column( )

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.email = kwargs.get('email','')
        self.year = kwargs.get('year')
        self.bio = kwargs.get('bio')
        self.looking_for_buddy = False
        

    def serialize(self):
        return {
            'id': self.id,
            'email' : self.email,
            'name': self.name,
            'year' : self.year,
            'bio' : self.bio,
            'looking': self.looking_for_buddy
        }




class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable = False)
    location = db.Column(db.String, nullable = False)
    host = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False) 
    guests = db.Column(db.Integer, )


    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.time = kwargs.get('time', '')
        self.location = kwargs.get('location', '')
        self.host = kwargs.get('host', '')


    def serialize(self):
        return {
            'id': self.id,
            'name' : self.name,
            'time': self.time,
            'location': self.location,
            'host': User.query.filter_by(id = self.host).first().name
        }




