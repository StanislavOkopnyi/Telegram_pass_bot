from telegram_pass_bot.pass_generator.pass_generator import get_password
import string

password = get_password


def test_pass_length():
    assert len(password(10)) == 10
    assert len(password(12)) == 12
    assert password(6) == "Password too short"
    assert len(password()) == 8
    assert len(password(20)) == 20
    assert len(password(50)) == 50


def test_pass_symbols():
    assert any(map(lambda x: x in string.ascii_uppercase, password()))
    assert any(map(lambda x: x in string.ascii_lowercase, password()))
    assert any(map(lambda x: x in string.digits, password()))
    assert any(map(lambda x: x in string.punctuation, password()))
