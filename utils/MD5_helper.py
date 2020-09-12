import hashlib


class MD5Helper(object):
    @classmethod
    def hash(cls, string: str) -> str:
        md5 = hashlib.md5()
        md5.update(string.encode("utf-8"))
        return md5.hexdigest()

    @classmethod
    def evaluate(cls, string, hash) -> bool:
        return cls.hash(string) == hash

