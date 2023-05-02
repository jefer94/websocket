import os

import redis


r = redis.Redis()

list = [1, 2, 3]
r.rpush("lst", *list)


def get_env():
    return os.getenv("ENV")


class Redis:
    ...


class Redis:
    ...


class InMemory:
    _client: redis.Redis
    _is_production: bool

    def __new__(cls):
        os.environ["REDIS_URL"] = "redis://localhost:6379"
        os.getenv("REDIS_URL")

        cls._is_production = get_env() == "production"

        if cls._is_production and not hasattr(cls, "_client"):
            cls._client = redis.Redis()

        elif not cls._is_production and not hasattr(cls, "_cache"):
            cls._cache = {}

        obj = super().__new__(cls)
        return obj

    @classmethod
    def get(cls, key):
        if cls._is_production:
            cls._client.json().get(key)

        else:
            cls._cache.get(key)

    @classmethod
    def set(cls, key, value):
        if cls._is_production:
            cls._client.json().set(key, "$", value)

        else:
            cls._cache.update({key: value})
