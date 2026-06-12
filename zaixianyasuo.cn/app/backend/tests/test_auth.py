"""Auth-related tests: password verify roundtrip, strength, tokens."""

import sys
import os
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.exceptions import HTTPException


def test_password_verify_roundtrip():
    from app.utils.security import get_password_hash, verify_password
    for pw in ("abc12345", "P@ssw0rd!", "a" * 64):
        h = get_password_hash(pw)
        assert verify_password(pw, h)
        assert not verify_password(pw + "x", h)


def test_validate_password_strength_edge_cases():
    from app.utils.security import validate_password_strength
    with pytest.raises(HTTPException):
        validate_password_strength("Ab1")  # too short
    with pytest.raises(HTTPException):
        validate_password_strength("")     # empty


def test_token_creation():
    from app.utils.security import create_access_token
    token = create_access_token({"sub": "42"})
    assert token
    assert len(token) > 10
