import time
from typing import Any, Tuple

class TTLCache:
    """
    Cache em memória simples com Time To Live (TTL).
    Armazena chave -> valor por um período configurado (ttl_seconds).
    """
    def __init__(self, ttl_seconds: int = 600):
        self.ttl = ttl_seconds
        self._data: dict[str, Tuple[float, Any]] = {}

    def get(self, key: str):
        now = time.time()
        if key in self._data:
            ts, val = self._data[key]
            if now - ts < self.ttl:
                return val
            else:
                # expirado → remove
                self._data.pop(key, None)
        return None

    def set(self, key: str, value: Any):
        self._data[key] = (time.time(), value)

    def clear(self):
        self._data.clear()
