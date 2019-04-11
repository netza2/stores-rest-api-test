from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username': 'test', 'password': '123'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully.'},
                                     json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '123'})
                auth_response = client.post('/auth',
                                           data=json.dumps({'username': 'test', 'password': '123'}),
                                           headers={'Content-Type': 'application/json'})     # Content-Type tells a web
                self.assertIn('access_token', json.loads(auth_response.data).keys())          # server what type of data                                                                                             # you're sending

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': '123'})
                response = client.post('/register', data={'username': 'test', 'password': '123'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'},
                                     json.loads(response.data))

