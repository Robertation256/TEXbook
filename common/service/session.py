from base import base_redis_dict
import flask
import uuid


class Session(base_redis_dict.BaseRedisDict):
    def __init__(self):
        session_id = flask.session.get("session_id")
        if session_id is None:
            session_id = str(uuid.uuid4())
            flask.session["session_id"] = session_id
        super().__init__(name=session_id)
