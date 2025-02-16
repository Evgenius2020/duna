import os
import pickle
from typing import Callable, Any


class InMemoryCache:
    def __init__(
        self,
        savefile: str = 'in_memory_cache.pkl',
    ):
        self._savefile: str = savefile
        self._cache: dict[str, Any] = {}
        self._new_records_counter = 0
        self._found_records_counter = 0

        if os.path.exists(self._savefile):
            with open(self._savefile, 'rb') as f:
                self._cache = pickle.load(f)

    def get(self, key: str, generation_func: Callable) -> Any:
        if key not in self._cache:
            self._new_records_counter += 1
            self._cache[key] = generation_func()
        else:
            self._found_records_counter += 1
        return self._cache[key]

    def save(self) -> None:
        with open(self._savefile, 'wb') as f:
            pickle.dump(self._cache, f)

    def get_stats(self):
        return {
            'total_records': len(self._cache),
            'new_records': self._new_records_counter,
            'found_records': self._found_records_counter,
        }
