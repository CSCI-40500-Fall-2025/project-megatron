import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient

import server.main as m


class TestSignUpEndpoint:

    @pytest.fixture(autouse=True)
    def clear_users(self):
        m.USERS.clear()
        yield

    def test_signup_success(self):
        client = TestClient(m.app)
        res = client.post('/signup', json={
            'email': 'mock@email.com',
            'password': 'mockpassword123!'
        })
        assert res.status_code == 200
        data = res.json()
        assert data['email'] == 'mock@email.com'
        assert 'created_at' in data

    def test_signup_duplicate(self):
        client = TestClient(m.app)
        client.post('/signup', json={'email': 'mock@email.com', 'password': 'mockpassword123!'})
        res = client.post('/signup', json={'email': 'mock@email.com', 'password': 'mockpassword123!'})
        assert res.status_code == 409

    def test_signup_weak_password(self):
        client = TestClient(m.app)
        res = client.post('/signup', json={'email': 'mock@example.com', 'password': 'invalid'})
        assert res.status_code == 400
        body = res.json()
        assert 'errors' in body['detail']
