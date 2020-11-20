from utils.redis_client import redis_client


class BaseRedisDict():

    def __init__(self, name:str):
        self.redis = redis_client
        self.name = name

    def get(self, key: str):
        result = self.redis.hget(name=self.name, key=key)
        if result is None:
            return
        return result.decode()

    def __setitem__(self, key, value):
        self.redis.hset(name=self.name, key=key, value=value)
        self.expire(600)

    def expire(self, seconds: int):
        self.redis.expire(name=self.name, time=seconds)

    def extend(self):
        self.expire(3600)

    def delete(self, key):
        self.redis.hdel(self.name, key)