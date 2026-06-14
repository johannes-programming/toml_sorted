import argparse
import logging
import sys
from collections.abc import Iterable
from typing import Any, Optional

import setdoc

from .run import run
from typing import TypeVar,Literal
__all__ = ["main"]
Value=TypeVar("Value")

def key(arg:str) -> tuple[Literal["key"], str]:
    return "key", arg

def index(arg:str) -> tuple[Literal["index"], int]:
    return "index", int(arg)



@setdoc.basic
def main(args: Optional[Iterable[str]] = None, /) -> None:
    kwargs: dict[str, Any]
    parser: argparse.ArgumentParser
    parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
    parser.add_argument(
        "filepatterns",
        default=[],
        nargs="*",
    )
    parser.add_argument(
        "--all-keys",
        action="append_const",
        const=("all-keys", None),
        dest="instructions",
    )
    parser.add_argument(
        "--all-indices",
        action="append_const",
        const=("all-indices", None),
        dest="instructions",
    )
    parser.add_argument(
        "--key",
        action="append",
        dest="instructions",
        type=key,
    )
    parser.add_argument(
        "--index",
        action="append",
        dest="instructions",
        type=index,
    )
    parser.add_argument(
        "--sort",
        action="append_const",
        const=("sort", False),
        dest="instructions",
    )
    parser.add_argument(
        "--sort-reverse",
        action="append_const",
        const=("sort", True),
        dest="instructions",
    )
    parser.set_defaults(instructions=[])
    kwargs = vars(parser.parse_args(args))
    try:
        run(*kwargs.pop("filepatterns"), **kwargs)
    except Exception:
        logging.exception("toml_sorted failed!")
        sys.exit(1)
