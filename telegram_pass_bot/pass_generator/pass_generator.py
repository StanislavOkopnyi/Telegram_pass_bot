from random import choice
import string


UPPER_CASE = string.ascii_uppercase
LOWER_CASE = string.ascii_lowercase
DIGITS = string.digits
PUNCTUATION = string.punctuation


def check_pass(pass_to_check: list):
    """Check if pass contain one upper case, 
       lower case, digit and puncutation """
    if not any(map(lambda x: x in string.ascii_uppercase, pass_to_check)):
        return (False, string.ascii_uppercase)
    elif not any(map(lambda x: x in string.ascii_lowercase, pass_to_check)):
        return (False, string.ascii_lowercase)
    elif not any(map(lambda x: x in string.digits, pass_to_check)):
        return (False, string.digits)
    elif not any(map(lambda x: x in string.punctuation, pass_to_check)):
        return (False, string.punctuation)
    return (True, "")


def get_password(length: int = 8) -> str:
    """Function generate password which always contains:
       one upper case, lower case, digit and puncutation.
       If length < 8 returns 'Password too short'."""
    if length < 8:
        return "Password too short"

    symbols = [UPPER_CASE, LOWER_CASE,
               DIGITS, PUNCTUATION]
    password = list()

    for _ in range(length):
        symb_type = choice(symbols)
        password.append(choice(symb_type))

    while not check_pass(password)[0]:
        elem_num = choice(list(range(length)))
        elem_symb = choice(check_pass(password)[1])
        password[elem_num] = elem_symb

    return "".join(password)
