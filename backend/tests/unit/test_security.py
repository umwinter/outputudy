from app.infrastructure.security import get_password_hash, verify_password


def test_password_hashing() -> None:
    password = "secret_password"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_password_different_for_same_input() -> None:
    password = "secret_password"
    hashed1 = get_password_hash(password)
    hashed2 = get_password_hash(password)

    # Salt should be different
    assert hashed1 != hashed2
