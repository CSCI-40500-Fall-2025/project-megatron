import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import server.auth as a


class TestAuth:
    
    def test_email_validation(self):
        """Valid and invalid email addresses are detected correctly."""

        assert a.is_valid_email('user@example.com')
        assert not a.is_valid_email('bad-email')
        assert not a.is_valid_email('')

    def test_valid_password(self):
        password = 'superawesomePW1!'
        valid, _ = a.is_strong_password(password)
        assert valid

    def test_password_too_short(self):
        password = 'short'
        _, error = a.is_strong_password(password)
        assert error[0] == 'password must be at least 12 characters'

    def test_password_no_digits(self):
        password = 'nodigitsbutlongenough'
        _, error = a.is_strong_password(password)
        assert error[0] == 'password must contain a number'
    
    def test_password_no_special_characters(self):
        password = 'nospecialcharsbut1andlongenough'
        _, error = a.is_strong_password(password)
        assert error[0] == 'password must contain a special character'
    