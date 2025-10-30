import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from server.main import is_valid_email, is_strong_password

class TestAuth:

    def test_email_validation(self):
        """Valid and invalid email addresses are detected correctly."""

        assert is_valid_email('user@example.com')
        assert not is_valid_email('bad-email')
        assert not is_valid_email('')

    def test_valid_password(self):
        password = 'superawesomePW1!'
        valid, _ = is_strong_password(password)
        assert valid

    def test_password_too_short(self):
        password = 'short'
        _, error = is_strong_password(password)
        assert error[0] == 'password must be at least 12 characters'

    def test_password_no_digits(self):
        password = 'nodigitsbutlongenough'
        _, error = is_strong_password(password)
        assert error[0] == 'password must contain a number'
    
    def test_password_no_special_characters(self):
        password = 'nospecialcharsbut1andlongenough'
        _, error = is_strong_password(password)
        assert error[0] == 'password must contain a special character'
    