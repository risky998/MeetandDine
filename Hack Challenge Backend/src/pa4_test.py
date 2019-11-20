import unittest
import json
import requests
from app import app
from threading import Thread
from time import sleep

# NOTE: Make sure you run 'pip3 install requests' in your virtualenv

# URL pointing to your local dev host
LOCAL_URL = 'http://localhost:5000'
CLASSBODY = {'code': 'CS 1998', 'name': 'Intro to Backend Development'}
USERBODY = {'name': 'Alicia Wang', 'netid': 'aw1234'}
ASSIGNMENTBODY = {'title': 'PA5', 'due_date': 1554076799}

class TestRoutes(unittest.TestCase):

    def test_get_initial_courses(self):
        res = requests.get(LOCAL_URL + '/api/courses/')
        assert res.json()['success']

    def test_create_course(self):
        res = requests.post(LOCAL_URL + '/api/courses/', data=json.dumps(CLASSBODY))
        course = res.json()['data']
        assert res.json()['success']
        assert course['code'] == 'CS 1998'
        assert course['name'] == 'Intro to Backend Development'
        assert course['assignments'] == []
        assert course['students'] == []
        assert course['instructors'] == []

    def test_get_course(self):
        res = requests.post(LOCAL_URL + '/api/courses/', data=json.dumps(CLASSBODY))
        course_id = res.json()['data']['id']
        res = requests.get(LOCAL_URL + '/api/course/' + str(course_id) + '/')
        assert res.json()['success']

    def test_create_user(self):
        res = requests.post(LOCAL_URL + '/api/users/', data=json.dumps(USERBODY))
        course = res.json()['data']
        assert res.json()['success']
        assert course['name'] == 'Alicia Wang'
        assert course['netid'] == 'aw1234'

    def test_get_user(self):
        res = requests.post(LOCAL_URL + '/api/users/', data=json.dumps(USERBODY))
        usr_id = res.json()['data']['id']
        res = requests.get(LOCAL_URL + '/api/user/' + str(usr_id) + '/')
        assert res.json()['success']
        user = res.json()['data']
        assert user['name'] == 'Alicia Wang'
        assert user['netid'] == 'aw1234'
        assert user['courses'] == []

    def test_add_student_to_course(self):
        res = requests.post(LOCAL_URL + '/api/courses/', data=json.dumps(CLASSBODY))
        course_id = res.json()['data']['id']
        res = requests.post(LOCAL_URL + '/api/users/', data=json.dumps(USERBODY))
        usr_id = res.json()['data']['id']
        body = {'type': 'student', 'user_id': usr_id}
        res = requests.post(LOCAL_URL + '/api/course/' + str(course_id) + '/add/',
                            data=json.dumps(body))
        assert res.json()['success']

        res = requests.get(LOCAL_URL + '/api/course/' + str(course_id) + '/')
        assert res.json()['success']
        students = res.json()['data']['students']
        assert len(students) == 1
        assert students[0]['name'] == 'Alicia Wang'

    def test_add_instructor_to_course(self):
        res = requests.post(LOCAL_URL + '/api/courses/', data=json.dumps(CLASSBODY))
        course_id = res.json()['data']['id']
        res = requests.post(LOCAL_URL + '/api/users/', data=json.dumps(USERBODY))
        usr_id = res.json()['data']['id']
        body = {'type': 'instructor', 'user_id': usr_id}
        res = requests.post(LOCAL_URL + '/api/course/' + str(course_id) + '/add/',
                            data=json.dumps(body))
        assert res.json()['success']

        res = requests.get(LOCAL_URL + '/api/course/' + str(course_id) + '/')
        assert res.json()['success']
        instructors = res.json()['data']['instructors']
        assert len(instructors) == 1
        assert instructors[0]['name'] == 'Alicia Wang'

    def test_create_assignment_for_course(self):
        res = requests.post(LOCAL_URL + '/api/courses/', data=json.dumps(CLASSBODY))
        course_id = res.json()['data']['id']
        res = requests.post(LOCAL_URL + '/api/course/' + str(course_id) + '/assignment/',
                            data=json.dumps(ASSIGNMENTBODY))
        assert res.json()['data']['title'] == 'PA5'
        assert res.json()['data']['due_date'] == 1554076799

    def test_get_invalid_course(self):
        res = requests.get(LOCAL_URL + '/api/course/1000/')
        assert not res.json()['success']

    def test_get_invalid_user(self):
        res = requests.get(LOCAL_URL + '/api/user/1000/')
        assert not res.json()['success']

    def test_add_user_invalid_course(self):
        body = {'type': 'instructor', 'user_id': 0}
        res = requests.post(LOCAL_URL + '/api/course/1000/add/', data=json.dumps(body))
        assert not res.json()['success']

    def test_create_assignment_invalid_course(self):
        res = requests.post(LOCAL_URL + '/api/course/1000/assignment/',
                            data=json.dumps(ASSIGNMENTBODY))
        assert not res.json()['success']

    def test_course_id_increments(self):
        res = requests.post(LOCAL_URL + '/api/courses/', data=json.dumps(CLASSBODY))
        course_id = res.json()['data']['id']

        res2 = requests.post(LOCAL_URL + '/api/courses/', data=json.dumps(CLASSBODY))
        course_id2= res2.json()['data']['id']

        assert course_id + 1 == course_id2

def run_tests():
    sleep(1.5)
    unittest.main()

if __name__ == '__main__':
    thread = Thread(target=run_tests)
    thread.start()
    app.run(host='0.0.0.0', port=5000, debug=False)
