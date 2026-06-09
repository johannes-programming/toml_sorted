import glob
import os
import tomllib
from collections.abc import Iterable
from typing import Any, cast

import tomli_w

from ..enum.Instruction import Instruction

__all__ = ["run"]


def go(
    *,
    instruction: Instruction,
    keys: list[int | str],
    data: dict[str, Any],
) -> dict[str, Any]:
    target: Any
    keys_ = list(keys)
    if not len(keys_):
        return cast(
            dict[str, Any],
            sort(
                data,
                reverse=instruction.value,
            ),
        )
    target = data
    while len(keys_) > 1:
        target = target[keys_.pop(0)]
    target[keys_[0]] = sort(
        target[keys_[0]],
        reverse=instruction.value,
    )
    return data


def parse_instructions(
    instructions: Iterable[Instruction | int | str] = (),
) -> list[tuple[Instruction, list[int | str]]]:
    ans: list[tuple[Instruction, list[int | str]]]
    x: Instruction | int | str
    ans = list()
    for x in instructions:
        if isinstance(x, Instruction):
            ans.append((x, list()))
        elif len(ans):
            ans[-1][1].append(x)
    return ans


def run(
    *filepatterns: str,
    instructions: Iterable[Instruction | int | str] = (),
) -> None:
    absfile: str
    absfiles: list[str]
    data: Any
    file: str
    parsed: list[tuple[Instruction, list[int | str]]]
    pattern: str
    parsed = parse_instructions(instructions)
    absfiles = list()
    for pattern in filepatterns:
        for file in glob.iglob(pattern, recursive=True):
            absfile = os.path.abspath(file)
            if absfile in absfiles:
                continue
            if os.path.isfile(absfile):
                absfiles.append(absfile)
    for absfile in absfiles:
        with open(absfile, "rb") as stream:
            data = tomllib.load(stream)
        for instruction, keys in parsed:
            data = go(
                data=data,
                instruction=instruction,
                keys=keys,
            )
        with open(absfile, "wb") as stream:
            tomli_w.dump(data, stream)


def sort(data: Any, *, reverse: bool) -> Any:
    if isinstance(data, dict):
        return dict(sorted(data.items(), reverse=reverse))
    if isinstance(data, list):
        return list(sorted(data, reverse=reverse))
    raise TypeError(
        f"Value {data!r} of type {type(data).__name__} cannot be sorted!"
    )
