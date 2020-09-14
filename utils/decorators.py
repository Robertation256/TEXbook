from utils.session import Session
from functools import wraps
from flask import redirect


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        session = Session()
        if session.get("logged_in") != "true":
            return redirect("/auth/login")
        session.extend()
        func(*args, **kwargs)
    return inner





