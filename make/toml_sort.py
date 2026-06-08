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
        "--infile",
        default="-",
        dest="infile",
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
    parser.add_argument(
        "--outfile",
        default="-",
        dest="outfile",
    )
    space = parser.parse_args(args)
    run(**vars(space))


def run(
    *,
    infile: str = "-",
    keys: Sequence[str] = (),
    reverse: bool = False,
    outfile: str = "-",
) -> None:
    data: dict[str, Any]
    key: int | str
    stream: Any
    target: Any
    if infile == "-":
        data = tomllib.loads(input())
    else:
        with open(infile, "rb") as stream:
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
    if outfile == "-":
        print(tomli_w.dumps(data), end="")
        return
    with open(outfile, "wb") as stream:
        tomli_w.dump(data, stream)


def sorted_data(*, data: Any, reverse: bool) -> Any:
    if isinstance(data, dict):
        return dict(sorted(data.items(), reverse=reverse))
    else:
        return type(data)(sorted(data, reverse=reverse))


if __name__ == "__main__":
    main()
