#!/usr/bin/env python3
"""
redis
"""
import redis
import uuid
from typing import Callable, Optional, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ count INCR """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wraper """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ history """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ rap god """
        class_name = self.__class__.__name__
        method_name = method.__name__
        input_key = f"{class_name}.{method_name}:inputs"
        output_key = f"{class_name}.{method_name}:outputs"

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, output)

        return output

    return wrapper


def replay(method: Callable) -> None:
    """history of calls of function"""
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(
            name, i.decode('utf-8'), o.decode('utf-8')))


class Cache():
    """ cache class """
    def __init__(self):
        """ init """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """store date """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self, key: str, fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, None]:
        """ make the data to its origin type """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_int(self, key):
        """ get int """
        return self.get(key, int)

    def get_str(self, key):
        """ get str """
        val = self._redis.get(key)
        return val.decode('utf-8')
