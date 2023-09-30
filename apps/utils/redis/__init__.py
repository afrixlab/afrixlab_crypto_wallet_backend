from django.conf import settings
from django.core.cache import cache


class RedisTools:
    _cache_key: str
    _timeout: int = settings.CACHE_TTL
    _cached_value = None

    def __init__(self, cache_key: str, ttl: int = None):
        self._cache_key = cache_key
        if ttl:
            self._timeout = ttl

    @staticmethod
    def redis_get(key: object, default: object = 0) -> object:
        return cache.get(key, default=default)

    @staticmethod
    def redis_set(key, value):
        if not value:
            cache.delete(key)
        cache.set(key, value)

    @property
    def cache_value(self):
        if self._cached_value:
            return self._cached_value
        value = cache.get(self._cache_key)
        self._cached_value = value
        return value

    @cache_value.setter
    def cache_value(self, value):
        if not value:
            cache.delete(self._cache_key)
        cache.set(self._cache_key, value, timeout=self._timeout)
        self._cached_value = value


class RedisCacheShortCuts:
    @staticmethod
    def set_cache_value(key: str, ttl: int, value: any):
        cache_instance = RedisTools(
            key,
            ttl=ttl,
        )
        cache_instance.cache_value = value
