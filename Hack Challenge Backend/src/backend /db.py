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
    events = db.relationship('Event', secondary=association_table, back_populates = 'users')
    events_hosting = []
    events_attending = []


    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.email = kwargs.get('email','')
        self.year = kwargs.get('year')
        self.bio = kwargs.get('bio')
        self.looking_for_buddy = False
        self.events_hosting = []
        self.events_attending = []
        

    def serialize(self):
        return {
            'id': self.id,
            'email' : self.email,
            'name': self.name,
            'year' : self.year,
            'bio' : self.bio,
            'looking': self.looking_for_buddy,
            'events_hosting': [a.alt_serialize() for a in self.events_hosting],
            'events_attending': [e.alt_serialize() for e in self.events_attending]

        }
    
    def alt_serialize(self):
        return {
            'id': self.id, 
            'name': self.name,
            'email': self.email,
            'year': self.year
        }



class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    time = db.Column(db.String, nullable = False)
    location = db.Column(db.String, nullable = False)
    users = db.relationship('User', secondary=association_table, back_populates = 'events')
    host = []
    guests = []

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.time = kwargs.get('time', '')
        self.location = kwargs.get('location', '')
        self.host = []
        self.guests = []


    def serialize(self):
        return {
            'id': self.id,
            'name' : self.name,
            'time': self.time,
            'location': self.location,
            'host': [h.alt_serialize() for h in self.host],
            'guests': [g.alt_serialize() for g in self.guests]
        }
    
    def alt_serialize(self): 
        return {
            'id': self.id, 
            'name': self.name,
            'time': self.time,
            'location': self.location
        }




