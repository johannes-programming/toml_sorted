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
        "files",
        nargs="*",
        default=[],
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
    files: Iterable[str] = (),
    *,
    targets: Optional[list[Optional[int | str]]] = None,
) -> None:
    file: str
    keyss: list[list[list]]
    keyss = parse_targets(targets)
    for file in files:
        for keys in keyss:
            go(file=file, keys=keys)


def parse_targets(targets: Optional[list[Optional[int | str]]] = None):
    ans: list[list[int | str]]
    ans = list()
    if targets is None:
        return ans
    for x in targets:
        if x is None:
            ans.append(list())
        elif len(ans):
            ans[-1].append(x)
    return ans


def go(
    file: str,
    *,
    keys: Sequence[int | str] = (),
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
            target = target[key]
        key = keys[-1]
        target[key] = sorted_data(data=target[key])
    else:
        data = sorted_data(data=data)
    if file == "-":
        print(tomli_w.dumps(data), end="")
        return
    with open(file, "wb") as stream:
        tomli_w.dump(data, stream)


def sorted_data(*, data: Any) -> Any:
    if isinstance(data, dict):
        return dict(sorted(data.items()))
    else:
        return type(data)(sorted(data))


if __name__ == "__main__":
    main()
