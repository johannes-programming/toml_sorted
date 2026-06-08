import argparse
import tomllib
from collections.abc import Iterable, Sequence
from typing import Any, Optional

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
        default=[],
        dest="keys",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
    )
    space = parser.parse_args(args)
    run(**vars(space))


def run(
    *,
    files: list[str],
    **kwargs: Any,
) -> None:
    file: str
    for file in files:
        run_file(file, **kwargs)


def run_file(
    file: str,
    *,
    keys: Sequence[str] = (),
    reverse: bool = False,
) -> None:
    data: dict[str, Any]
    key: int | str
    stream: Any
    target: Any
    if file == "-":
        data = tomllib.loads(input())
    else:
        with open(file, "rb") as stream:
            data = tomllib.load(stream)
    if len(keys):
        target = data
        for key in keys[:-1]:
            target = target[str(key) if isinstance(target, dict) else int(key)]
        if isinstance(target, dict):
            key = str(keys[-1])
        else:
            key = int(keys[-1])
        target[key] = sorted_data(data=target[key], reverse=reverse)
    else:
        data = sorted_data(data=data, reverse=reverse)
    if file == "-":
        print(tomli_w.dumps(data), end="")
        return
    with open(file, "wb") as stream:
        tomli_w.dump(data, stream)


def sorted_data(*, data: Any, reverse: bool) -> Any:
    if isinstance(data, dict):
        return dict(sorted(data.items(), reverse=reverse))
    else:
        return type(data)(sorted(data, reverse=reverse))


if __name__ == "__main__":
    main()
