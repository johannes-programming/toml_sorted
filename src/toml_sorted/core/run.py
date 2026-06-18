import glob
import os
import tomllib
from collections.abc import Iterable
from typing import Any, cast

import setdoc
import tomli_w

from toml_sorted.enum.Instruction import Instruction
from toml_sorted.enum.Selector import Selector

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
    instructions: Iterable[Instruction | Selector | int | str] = (),
) -> list[tuple[Instruction, list[Selector | int | str]]]:
    ans: list[tuple[Instruction, list[Selector | int | str]]]
    x: Instruction | Selector | int | str
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
    instructions: Iterable[Instruction | Selector | int | str] = (),
) -> None:
    absfiles: list[str]
    parsed: list[tuple[Instruction, list[Selector | int | str]]]
    parsed = parse_instructions(instructions)
    absfiles = get_absfiles(filepatterns)
    run_instructions_on_files(absfiles=absfiles, parsed=parsed)


def run_instruction_on_data(
    *,
    instruction: Instruction,
    keys: list[Selector | int | str],
    data: dict[str, Any],
) -> dict[str, Any]:
    return cast(
        dict[str, Any],
        run_instruction_along_keys(
            data,
            instruction=instruction,
            keys=list(keys),
        ),
    )


def run_instruction_along_keys(
    data: Any,
    *,
    instruction: Instruction,
    keys: list[Selector | int | str],
) -> Any:
    head: Selector | int | str
    rest: list[Selector | int | str]
    if not len(keys):
        return run_instruction_on_value(data, reverse=instruction.value)
    head = keys[0]
    rest = keys[1:]
    if head is Selector.ALL_KEYS:
        return run_instruction_on_all_keys(
            data,
            instruction=instruction,
            keys=rest,
        )
    if head is Selector.ALL_INDICES:
        return run_instruction_on_all_indices(
            data,
            instruction=instruction,
            keys=rest,
        )
    data[head] = run_instruction_along_keys(
        data[head],
        instruction=instruction,
        keys=rest,
    )
    return data


def run_instruction_on_all_keys(
    data: Any,
    *,
    instruction: Instruction,
    keys: list[Selector | int | str],
) -> Any:
    index: int
    key: Any
    if isinstance(data, dict):
        for key in list(data.keys()):
            data[key] = run_instruction_along_keys(
                data[key],
                instruction=instruction,
                keys=keys,
            )
        return data
    raise TypeError(
        f"Value {data!r} of type {type(data).__name__} has no keys to expand!"
    )


def run_instruction_on_all_indices(
    data: Any,
    *,
    instruction: Instruction,
    keys: list[Selector | int | str],
) -> Any:
    index: int
    if isinstance(data, list):
        for index in range(len(data)):
            data[index] = run_instruction_along_keys(
                data[index],
                instruction=instruction,
                keys=keys,
            )
        return data
    raise TypeError(
        f"Value {data!r} of type {type(data).__name__} has no indices to expand!"
    )


def run_instruction_on_value(data: Any, *, reverse: bool) -> Any:
    if isinstance(data, dict):
        return dict(sorted(data.items(), reverse=reverse))
    if isinstance(data, list):
        return list(sorted(data, reverse=reverse))
    raise TypeError(
        f"Value {data!r} of type {type(data).__name__} cannot be sorted!"
    )


def run_instructions_on_files(
    *,
    absfiles: list[str],
    parsed: list[tuple[Instruction, list[Selector | int | str]]],
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
