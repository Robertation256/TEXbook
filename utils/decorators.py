import uuid
from flask import session as flask_session, redirect, url_for
from utils.session import Session as redis_session
from functools import wraps


def post(func):
    if hasattr(func, "methods"):
        func.methods.append("POST")
    else:
        setattr(func, "methods", ["POST"])
    setattr(func, "__name__", "".join(func.__name__.split("_")[1:]))
    return func


def get(func):
    if hasattr(func, "methods"):
        func.methods.append("GET")
    else:
        setattr(func, "methods", ["GET"])
    setattr(func, "__name__", "_".join(func.__name__.split("_")[1:]))
    return func




