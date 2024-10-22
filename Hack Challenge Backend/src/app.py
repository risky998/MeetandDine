import json
from db import db, User, Event
from flask import Flask, request
import datetime

db_filename = "dine.db"
app = Flask(__name__)
# Db = db.DB()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/api/register/', methods = ['POST'])
def register_user(): 
    post_body = json.loads(request.data)
    name = post_body.get('name', '')
    email = post_body.get('email', '')
    year = post_body.get('year', '')
    bio = post_body.get('bio', '')

    user = User(
        name = name,
        email = email, 
        year = year, 
        bio = bio
    )

    db.session.add(user)
    db.session.commit()
    return json.dumps({'success': True, 'data' : user.serialize()}), 201



@app.route('/api/users/', methods = ['GET'])
def get_all_users(): 
    users = User.query.all()
    res = {'success': True, 'data': [u.alt_serialize() for u in users]}
    return json.dumps(res), 200

@app.route('/api/users/<int:user_id>', methods = ['GET'])
def get_user_by_username(user_id):
    user = User.query.filter_by(id = user_id).first()
    return json.dumps({'success': True, 'data':user.serialize()}), 200


@app.route('/api/users/dinner_seekers/')
def get_all_dinner_seekers(): 
    users = User.query.filter_by(looking_for_buddy = '1').all()
    res = {'success': True, 'data': [u.serialize() for u in users]}
    return json.dumps(res), 200


@app.route('/api/users/<int:user_id>/create_event/', methods = ['POST'])
def create_dinner_event(user_id):
    user = User.query.filter_by(id = user_id).first()
    if not user: 
        return json.dumps({'success': False, 'error':'User not found!'}), 404

    post_body = json.loads(request.data)
    name = post_body.get('name', '')
    time = post_body.get('time', '')
    location = post_body.get('location', '')

    event = Event(
        name = name,
        time = time,
        location = location,
    )

    event.host.append(user)
    db.session.add(event)
    user.events_hosting.append(event)
    db.session.commit()
    
    return json.dumps({'success': True, 'data':event.serialize()}), 200

@app.route('/api/events/', methods = ['GET'])
def get_all_events(): 
    events = Event.query.all()
    res = {'success': True, 'data': [u.alt_serialize() for u in events]}
    return json.dumps(res), 200


@app.route('/api/events/<int:event_id>/join', methods = ['POST'])
def join_dinner_event(event_id):
   
    event = Event.query.filter_by(id = event_id).first()

    post_body = json.loads(request.data)
    user_id = post_body.get('user_id')

    user = User.query.filter_by(id = user_id).first()
    if not user:
        return json.dumps({'success': False, 'error':'User not found!'}), 404
    
    if not event:
        return json.dumps({'success': False, 'error':'Event not found!'}), 404
    
    event.guests.append(user)
    user.events_attending.append(event)
    db.session.commit()

    return json.dumps({'success': True, 'data':event.serialize()}), 200



#get users attending a particular event 
#get events by user
@app.route('/api/events/<int:event_id>', methods = ['GET'])
def get_event_details(event_id): 
    event = Event.query.filter_by(id=event_id).first()
    if not event: 
        return json.dumps({'success': False, 'error':'Event not found!'}), 404
    
    print(event.name)
    print(event.host)
    return json.dumps({'success': True, 'data': event.serialize()})


@app.route('/api/users/<int:user_id>/hosting', methods = ['GET'])
def get_hosting_events(user_id):
    user = User.query.filter_by(id = user_id).first()
    if not user:
        return json.dumps({'success': False, 'error':'User not found!'}), 404

    return json.dumps({'success': True, 'data':[u.alt_serialize() for u in user.events_hosting]}), 200

@app.route('/api/users/<int:user_id>/attending', methods = ['GET'])
def get_attending_events(user_id):
    user = User.query.filter_by(id = user_id).first()
    if not user:
        return json.dumps({'success': False, 'error':'User not found!'}), 404
    
    return json.dumps({'success': True, 'data':[u.alt_serialize() for u in user.events_attending]}), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
