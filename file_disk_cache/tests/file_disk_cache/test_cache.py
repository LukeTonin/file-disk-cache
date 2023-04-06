from __future__ import annotations
import os
import pandas as pd

import pytest
from diskcache import Cache

from file_disk_cache.cache import call_with_cache
from file_disk_cache.file_disk import FileDisk


test_cases = [
    ({"s": 1}, "dir/something.json", "tmp_path"),
    (pd.DataFrame({"a": range(10)}), "dir/something.parquet", "tmp_path"),
    (pd.DataFrame({"a": range(10)}), "dir/something.csv", "tmp_path"),
]


@pytest.mark.parametrize("value, key, tmp_path", test_cases, indirect=["tmp_path"])
def test_add_and_get(value: Any, key: str, tmp_path: str):

    cache = Cache(directory=tmp_path, disk=FileDisk)

    cache.add(key=key, value=value)

    assert os.path.exists(os.path.join(tmp_path, key))

    value_fetched = cache.get(key=key)

    if isinstance(value, pd.DataFrame):
        assert value.equals(value_fetched)
    else:
        assert value == value_fetched


test_cases = [
    (lambda: {"s": 10}, "path.json", "tmp_path"),
]


@pytest.mark.parametrize("func, path, tmp_path", test_cases, indirect=["tmp_path"])
def test_call_with_cache(func: Any, path: str, tmp_path: str):

    cache = Cache(directory=tmp_path, disk=FileDisk)

    output1 = call_with_cache(func=func, path=path, cache=cache)

    assert os.path.exists(os.path.join(tmp_path, path))

    output2 = call_with_cache(func=func, path=path, cache=cache)

    if isinstance(output1, pd.DataFrame):
        assert output1.equals(output2)
    else:
        assert output1 == output2
