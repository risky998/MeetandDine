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
    res = {'success': True, 'data': [u.serialize() for u in users]}
    return json.dumps(res), 200



@app.route('/api/users/dinner_seekers/')
def get_all_dinner_seekers(): 
    users = User.query.filter_by(looking_for_buddy = '1').all()
    res = {'success': True, 'data': [u.serialize() for u in users]}
    return json.dumps(res), 200


@app.route('/api/users/<int:user_id>/create_event', methods = ['POST'])
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
        host = user_id
    )

    db.session.add(event)
    db.session.commit()
    return json.dumps({'success': True, 'data':event.serialize()}), 200






# @app.route('/api/user/<int:user_id>/')
# def get_user(user_id):
#     user = User.query.filter_by(id=user_id).first()
#     if not user:
#         return json.dumps({'success': False, 'error':'User not found!'}), 404
#     return json.dumps({'success': True, 'data':user.serialize()}), 200


# @app.route('/api/course/<int:course_id>/add/', methods = ['POST'])
# def add_user(course_id):
#     course = Course.query.filter_by(id = course_id).first()
#     if not Course:
#         return json.dumps({'success': False, 'error':'Course not found!'}), 404

#     post_body = json.loads(request.data)
#     type = post_body.get('type')
#     user_id = post_body.get('user_id')
#     user = User.query.filter_by(id=user_id).first()
#     if not user:
#         return json.dumps({'success': False, 'error':'User not found!'}), 404

#     if type == 'instructor':
#         course.users.append(user)
#         user.courses.append(course)
#         course.instructors.append(user)
#         db.session.commit()
#         return json.dumps({'success': True, 'data':course.serialize()}), 200

#     if type == 'student':
#         course.users.append(user)
#         user.courses.append(course)
#         course.students.append(user)
#         db.session.commit()
#         return json.dumps({'success': True, 'data':course.serialize()}), 200
#     else:
#         return json.dumps({'success': False, 'error':'Invalid User Type!'}), 404




# @app.route('/api/course/<int:course_id>/assignment/', methods = ['POST'])
# def create_assignment(course_id):
#     course = Course.query.filter_by(id=course_id).first()
#     if not course:
#         return json.dumps({'success': False, 'error':'Course not found!'}), 404

#     post_body = json.loads(request.data)
#     title = post_body.get('title', '')
#     due_date = post_body.get('due_date', '')
#     course_id = course_id

#     assignment = Assignment(
#         title = title,
#         due_date = due_date,
#         course = course_id
#     )
#     course.assignments.append(assignment)
#     db.session.add(assignment)
#     db.session.commit()
#     return json.dumps({'success': True, 'data':assignment.serialize()}), 200







if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)
