from utils.redis_client import redis_client
import flask
import uuid


class Session(object):
    def __init__(self):
        session_id = flask.session.get("session_id")
        self.redis = redis_client
        if session_id is None:
            session_id = str(uuid.uuid4())
            flask.session["session_id"] = session_id
        self.session_id = session_id

    def get(self, key: str):
        result = self.redis.hget(name=self.session_id, key=key)
        if result is None:
            return
        return result.decode()

    def __setitem__(self, key, value):
        print("set redis: ", (key, value))
        self.redis.hset(name=self.session_id, key=key, value=value)
        self.expire(600)

    def expire(self, seconds: int):
        self.redis.expire(name=self.session_id, time=seconds)

    def extend(self):
        self.expire(3600)