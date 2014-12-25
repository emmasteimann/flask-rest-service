from app import app
from app import db
from models import *
from flask import json
import unittest

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client(self)
        db.create_all()

    def tearDown(self):
        db.session.expunge_all()
        try:
            db.session.query(User).delete()
            db.session.query(UserGroup).delete()
            db.session.query(Group).delete()
            db.session.commit()
        except:
            db.session.rollback()

    #  GET /
    def test_index(self):
        response = self.tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    #  GET /users before adding
    def test_user_index(self):
        response = self.tester.get('/users', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_user_creation(self):
        #  POST Users
        response = self.tester.post('/users/jdoe', data=json.dumps(dict(
            first_name="John",
            last_name="Doe",
            userid="jdoe"
        )), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #  POST Users
        should_now_exist = self.tester.post('/users/jdoe', data=json.dumps(dict(
            first_name="John",
            last_name="Doe",
            userid="jdoe"
        )), content_type='application/json')
        self.assertEqual(should_now_exist.status_code, 409)

        #  GET /users after adding
        response = self.tester.get('/users/jdoe', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        # Users has John
        self.assertIn(b'John', response.data)

    def test_user_update(self):
        #  POST Users
        response = self.tester.post('/users/jdoe', data=json.dumps(dict(
            first_name="John",
            last_name="Doe",
            userid="jdoe"
        )), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #  PUT Users
        should_now_be_updated = self.tester.put('/users/jdoe', data=json.dumps(dict(
            first_name="Jane",
            last_name="Doe",
            userid="jdoe"
        )), content_type='application/json')
        self.assertEqual(should_now_be_updated.status_code, 202)

        #  GET /users/jdoe after adding
        response = self.tester.get('/users/jdoe', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        # Users has Jane, not John
        self.assertIn(b'Jane', response.data)
        self.assertNotIn(b'John', response.data)

    def test_user_delete(self):
        #  POST Users
        response = self.tester.post('/users/jdoe', data=json.dumps(dict(
            first_name="John",
            last_name="Doe",
            userid="jdoe"
        )), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #  DELETE Users
        should_now_be_deleted = self.tester.delete('/users/jdoe')
        self.assertEqual(should_now_be_deleted.status_code, 200)

        #  GET /users after adding
        response = self.tester.get('/users/jdoe', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    def test_group_creation(self):
        #  POST Groups
        response = self.tester.post('/groups/test_group', data=json.dumps(dict(
            name="test_group"
        )), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #  POST Groups
        should_now_exist = self.tester.post('/groups/test_group', data=json.dumps(dict(
            name="test_group"
        )), content_type='application/json')
        self.assertEqual(should_now_exist.status_code, 409)

        #  GET /groups after adding
        response = self.tester.get(
            '/groups/test_group', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        # Group has test_group
        self.assertIn(b'test_group', response.data)

    def test_group_update(self):
        #  POST Groups
        response = self.tester.post('/groups/test_group', data=json.dumps(dict(
            name="test_group"
        )), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # PUT Groups
        # Can update name
        should_now_be_updated = self.tester.put('/groups/test_group', data=json.dumps(dict(
            name="fancy_group"
        )), content_type='application/json')
        self.assertEqual(should_now_be_updated.status_code, 202)

        #  GET /groups/test_group should be missing
        response = self.tester.get(
            '/groups/test_group', content_type='html/text')
        self.assertEqual(response.status_code, 404)

        #  GET /groups/fancy_group should be missing
        response = self.tester.get(
            '/groups/fancy_group', content_type='html/text')
        self.assertEqual(response.status_code, 200)

        # Can add users
        # POST Users
        response = self.tester.post('/users/jdoe', data=json.dumps(dict(
            first_name="John",
            last_name="Doe",
            userid="jdoe"
        )), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # PUT Groups
        # Can update name
        response = self.tester.put('/groups/fancy_group', data=json.dumps(dict(
            name="fancy_group",
            users=['jdoe']
        )), content_type='application/json')
        self.assertEqual(response.status_code, 202)

        #  GET /groups/fancy_group
        response = self.tester.get(
            '/groups/fancy_group', content_type='html/text')
        self.assertIn(b'jdoe', response.data)

    def test_group_delete(self):
        #  POST Users
        response = self.tester.post('/groups/fancy_group', data=json.dumps(dict(
            name="fancy_group",
        )), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        #  DELETE Users
        should_now_be_deleted = self.tester.delete('/groups/fancy_group')
        self.assertEqual(should_now_be_deleted.status_code, 200)

        #  GET /users after adding
        response = self.tester.get(
            '/groups/fancy_group', content_type='html/text')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
