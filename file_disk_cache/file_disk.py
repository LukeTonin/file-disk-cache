from __future__ import annotations
import os
import pathlib
import io
import json
import dataclasses

import pandas as pd

import diskcache
from diskcache.core import UNKNOWN


class NoValidModeError(Exception):
    pass


def save_json(obj: dict, path: str) -> None:

    with open(path, "w") as f:
        json.dump(obj=obj, fp=f)


def load_json(path: str) -> Union[dict, str]:
    with open(path, "rb") as f:
        obj = json.load(fp=f)

    return obj


@dataclasses.dataclass
class Mode:
    id_: int
    file_suffix: str
    types: tuple[type]
    save_func: callable
    load_func: callable


DEFAULT_MODES = [
    Mode(
        id_=5,
        file_suffix=".parquet",
        types=(pd.DataFrame,),
        save_func=lambda df, path: df.to_parquet(path),
        load_func=pd.read_parquet,
    ),
    Mode(
        id_=6,
        file_suffix=".csv",
        types=(pd.DataFrame, pd.Series),
        save_func=lambda df, path: df.to_csv(path),
        load_func=lambda path: pd.read_csv(path, index_col=0),
    ),
    Mode(
        id_=7,
        file_suffix=".json",
        types=(dict, list),
        save_func=save_json,
        load_func=load_json,
    ),
]


class FileDisk(diskcache.Disk):
    """An extension of the basic diskcache disk that"""

    def __init__(
        self,
        directory,
        modes: list[Mode] = DEFAULT_MODES,
        min_file_size: int = 0,
        pickle_protocol: int = 0,
    ):

        self.modes = modes

        super().__init__(directory, min_file_size, pickle_protocol)

    def store(self, value: Any, read: bool, key: Any = UNKNOWN):
        if key == UNKNOWN or not isinstance(key, str):
            raise ValueError(f"This cache can only be called with string keys. Received: {key}")

        if read:
            raise ValueError(f"This cache cannot be called with read == True")

        for mode in self.modes:
            if key.endswith(mode.file_suffix) and isinstance(value, mode.types):
                path = pathlib.Path(self._directory, key)
                path.parent.mkdir(parents=True, exist_ok=True)
                mode.save_func(value, path)
                size = os.path.getsize(path)

                return size, mode.id_, key, None

        raise NoValidModeError("Could not find a valid write mode for the provided key and value.")

    def fetch(self, mode: int, filename: str, value: Any, read: bool):
        for mode_ in self.modes:
            if mode == mode_.id_:
                return mode_.load_func(os.path.join(self._directory, filename))

        raise NoValidModeError(
            f"Could not find and acceptable method for the provided filename: {filename} and mode: {mode}"
        )
