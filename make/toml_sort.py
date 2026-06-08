import argparse
import tomllib
from collections.abc import Iterable
from typing import Any, Optional
import os
from pathlib import Path

import tomli_w

__all__ = ["main", "run"]


def main(args: Optional[Iterable[str]] = None, /) -> None:
    parser: argparse.ArgumentParser
    space: argparse.Namespace
    parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
    parser.add_argument(
        "--file",
        action="append",
        default=[],
        dest="files",
    )
    parser.add_argument(
        "--key",
        action="append",
        dest="targets",
    )
    parser.add_argument(
        "--index",
        action="append",
        dest="targets",
        type=int,
    )
    parser.add_argument(
        "--sort",
        action="append_const",
        const=None,
        dest="targets",
    )
    space = parser.parse_args(args)
    run(**vars(space))


def run(
    *,
    files: Iterable[str] = (),
    targets: Iterable[Optional[int | str]] = (),
) -> None:
    pattern:str
    targets_:list[list[Optional[int | str]]]
    x:Optional[int | str]
    targets_ = []
    for x in targets:
        if x is None:
            targets_.append([])
        elif len(targets_):
            targets_[-1].append(x)
    for pattern in files:
        for path in Path(os.getcwd()).glob(pattern):
            with open(path, "rb") as stream:
                data = tomllib.load(stream)
            for target in targets_:
                sort(data, target=target)
            with open(path, "wb") as stream:
                tomli_w.dump(data, stream)

def sort(
        data:Any,
        *,
        target:list[int | str],
) -> None:
    data_: Any
    dict_:Any
    data_ = data
    for x in target:
        data_=data_[x]
    if isinstance(data_, dict):
        dict_=dict(sorted(data_.items()))
        data_.clear()
        data_.update(dict_)
    else:
        data_.sort()

if __name__ == "__main__":
    main()