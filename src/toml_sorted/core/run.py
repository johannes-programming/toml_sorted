import glob
import os
import tomllib
from collections.abc import Iterable
from typing import Any, cast, Literal

import setdoc
import tomli_w

__all__ = ["run"]


def parse_filepatterns(filepatterns: Iterable[str]) -> list[str]:
    absfile: str
    absfiles: list[str]
    file: str
    pattern: str
    absfiles = list()
    for pattern in filepatterns:
        for file in glob.iglob(pattern, recursive=True):
            absfile = os.path.abspath(file)
            if absfile in absfiles:
                continue
            if os.path.isfile(absfile):
                absfiles.append(absfile)
    return absfiles


def parse_instructions(
    instructions: Iterable[Any] = (),
) -> list[Any]:
    ans: list[Any]
    x: Literal["all-keys", "all-indices", "index", "key", "sort"]
    y: bool | int | str
    ans = list()
    for x, y in instructions:
        if x == "sort":
            ans.append(((x, y), []))
        elif len(ans):
            ans[-1][-1].append((x, y))
    return ans


@setdoc.basic
def run(
    *filepatterns: str,
    instructions: Iterable[
        tuple[Literal["all-keys"], None],
        tuple[Literal["all-indices"], None],
        tuple[Literal["index"], int],
        tuple[Literal["key"], str],
        tuple[Literal["sort"], bool],
    ] = (),
) -> None:
    absfiles: list[str]
    parsed: list[Any]
    parsed = parse_instructions(instructions)
    absfiles = parse_filepatterns(filepatterns)
    process_all(absfiles=absfiles, parsed=parsed)



def process_all(
    *,
    absfiles: list[str],
    parsed: Iterable[Any],
) -> None:
    absfile: str
    data: Any
    for absfile in absfiles:
        with open(absfile, "rb") as stream:
            data = tomllib.load(stream)
        for (name, mark), lines in parsed:
            data = process_cmd(
                data=data,
                name=name,
                mark=mark,
                lines=lines,
            )
        with open(absfile, "wb") as stream:
            tomli_w.dump(data, stream)

def process_cmd(
    *,
    lines:list[Any],
    name: Literal["sort"],
    **kwargs:Any,
) -> dict[str, Any]:
    lines_:list[list[Any]]
    if name == "sort":
        return process_cmd_sort(**kwargs)
    raise ValueError

def process_cmd_sort(
    *,
    data: dict[str, Any],
    mark: Any,
    lines:list[tuple[Any, Any]],
) -> dict[str, Any]:
    if not lines:
        return sort(
            data,
            reverse=mark,
        )
    target = data
    while len(lines) > 1:
        target = target[lines.pop(0)[1]]
    target[lines[0]] = sort(
        target[lines[0]],
        reverse=mark,
    )
    return data


def sort(data: Any, *, reverse: bool) -> Any:
    if isinstance(data, dict):
        return dict(sorted(data.items(), reverse=reverse))
    if isinstance(data, list):
        return list(sorted(data, reverse=reverse))
    raise TypeError(
        f"Value {data!r} of type {type(data).__name__} cannot be sorted!"
    )
