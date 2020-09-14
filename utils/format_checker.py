import re
from common.models.user import User


def nyu_email_check(email: str) -> bool:
    pattern = re.compile("^[A-Za-z0-9]{4,}@nyu.edu$")
    if pattern.match(email):
        return True
    else:
        return False


def username_checker(username: str):
    if len(username) not in range(4,20):
        return {"status": False, "error": "wrong username format"}
    if User.select().where(User.username == username).exists():
        return {"status": False, "error": "username exists"}
    return {"status": True, "error": "wrong username format"}


def password_checker(password: str) -> bool:
    if len(password) not in range(6,16):
        return False
    return True
