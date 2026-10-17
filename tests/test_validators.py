from app import validators as v


def test_username_valid_and_invalid():
    assert v.validate_username("budi_01") is None
    assert v.validate_username("a") is not None
    assert v.validate_username("bad name!") is not None
    assert v.validate_username(123) is not None


def test_password_rules():
    assert v.validate_password("abc12345") is None
    assert v.validate_password("short1") is not None
    assert v.validate_password("hanyahuruf") is not None
    assert v.validate_password("12345678") is not None


def test_note_rules():
    assert v.validate_note("Judul", "isi") is None
    assert v.validate_note("  ", "isi") is not None
    assert v.validate_note("x" * 101, "isi") is not None
    assert v.validate_note("ok", 5) is not None
    assert v.validate_note("ok", "y" * 5001) is not None
