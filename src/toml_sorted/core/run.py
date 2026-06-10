import glob
import os
import tomllib
from collections.abc import Iterable
from typing import Any, cast

import setdoc
import tomli_w

from ..enum.Instruction import Instruction

__all__ = ["run"]


def get_absfiles(filepatterns: Iterable[str]) -> list[str]:
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


@setdoc.basic
def run(
    *filepatterns: str,
    instructions: Iterable[Instruction | int | str] = (),
) -> None:
    absfiles: list[str]
    parsed: list[tuple[Instruction, list[int | str]]]
    parsed = parse_instructions(instructions)
    absfiles = get_absfiles(filepatterns)
    run_instructions_on_files(absfiles=absfiles, parsed=parsed)


def run_instruction_on_data(
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
            run_instruction_on_value(
                data,
                reverse=instruction.value,
            ),
        )
    target = data
    while len(keys_) > 1:
        target = target[keys_.pop(0)]
    target[keys_[0]] = run_instruction_on_value(
        target[keys_[0]],
        reverse=instruction.value,
    )
    return data


def run_instructions_on_files(
    *,
    absfiles: list[str],
    parsed: list[tuple[Instruction, list[int | str]]],
) -> None:
    absfile: str
    data: Any
    for absfile in absfiles:
        with open(absfile, "rb") as stream:
            data = tomllib.load(stream)
        for instruction, keys in parsed:
            data = run_instruction_on_data(
                data=data,
                instruction=instruction,
                keys=keys,
            )
        with open(absfile, "wb") as stream:
            tomli_w.dump(data, stream)


def run_instruction_on_value(data: Any, *, reverse: bool) -> Any:
    if isinstance(data, dict):
        return dict(sorted(data.items(), reverse=reverse))
    if isinstance(data, list):
        return list(sorted(data, reverse=reverse))
    raise TypeError(
        f"Value {data!r} of type {type(data).__name__} cannot be sorted!"
    )
