"""Security-related tests: password hashing, XSS detection, tokens."""

import sys
import os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.exceptions import HTTPException
from app.utils.security import get_password_hash, verify_password, validate_password_strength, normalize_username, normalize_email
from app.utils.tokens import new_token


def test_password_hash_and_verify():
    pwd = "TestP@ss123"
    h = get_password_hash(pwd)
    assert h != pwd
    assert verify_password(pwd, h)
    assert not verify_password("wrong", h)


def test_password_strength_ok():
    validate_password_strength("Abc12345")  # does not raise = valid


def test_password_strength_too_short():
    with pytest.raises(HTTPException):
        validate_password_strength("short")


def test_password_strength_only_digits():
    with pytest.raises(HTTPException):
        validate_password_strength("12345678")


def test_normalize_username():
    assert normalize_username("  hello  ") == "hello"


def test_normalize_email():
    assert normalize_email("  User@Example.COM  ") == "user@example.com"


def test_token_is_string():
    t = new_token(32)
    assert isinstance(t, str)
    assert len(t) > 0
    assert t != new_token(32)


def test_xss_rejected_in_username():
    xss = '<script>alert("xss")</script>'
    with pytest.raises(HTTPException):
        normalize_username(xss)
