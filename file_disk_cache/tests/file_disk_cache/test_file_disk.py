from __future__ import annotations
import os

import pytest
import pandas as pd

from file_disk_cache.file_disk import FileDisk, NoValidModeError


def test_raises_ValueError(tmp_path: str):
    file_disk = FileDisk(directory=tmp_path)
    with pytest.raises(expected_exception=ValueError):
        file_disk.store(value=1, read=True, key="something.json")


test_cases = [
    ({"s": 1}, False, "something", "tmp_path"),
    ({"s": 1}, False, "something.other", "tmp_path"),
    (1, False, "something.json", "tmp_path"),
    ({"s": 1}, False, "something.parquet", "tmp_path"),
]


@pytest.mark.parametrize("value, read, key, tmp_path", test_cases, indirect=["tmp_path"])
def test_raises_NoValidModeError(value: Any, read: bool, key: str, tmp_path: str):
    file_disk = FileDisk(directory=tmp_path)
    with pytest.raises(expected_exception=NoValidModeError):
        file_disk.store(value=value, read=read, key=key)


test_cases = [
    ({"s": 1}, False, "dir/something.json", "tmp_path"),
    (pd.DataFrame([[1]], columns=["name"]), False, "dir/something.parquet", "tmp_path"),
    (pd.DataFrame([[1]], columns=["name"]), False, "dir/something.csv", "tmp_path"),
]


@pytest.mark.parametrize("value, read, key, tmp_path", test_cases, indirect=["tmp_path"])
def test_store_and_fetch(value: Any, read: bool, key: str, tmp_path: str):
    file_disk = FileDisk(directory=tmp_path)
    size, mode, filename, value_ = file_disk.store(value=value, read=read, key=key)

    assert os.path.exists(os.path.join(tmp_path, key))

    value_fetched = file_disk.fetch(mode=mode, filename=filename, value=value_, read=read)

    if isinstance(value, pd.DataFrame):
        assert value.equals(value_fetched)
    else:
        assert value == value_fetched
