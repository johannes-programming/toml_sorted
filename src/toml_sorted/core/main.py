import argparse
import logging
import sys
from collections.abc import Iterable
from typing import Any, Optional

import setdoc

from ..enum.Instruction import Instruction
from .run import run

__all__ = ["main"]


@setdoc.basic
def main(args: Optional[Iterable[str]] = None, /) -> None:
    kwargs: dict[str, Any]
    parser: argparse.ArgumentParser
    parser = argparse.ArgumentParser(fromfile_prefix_chars="@")
    parser.add_argument(
        "filepatterns",
        nargs="*",
        default=[],
    )
    parser.add_argument(
        "--key",
        action="append",
        dest="instructions",
    )
    parser.add_argument(
        "--index",
        action="append",
        dest="instructions",
        type=int,
    )
    parser.add_argument(
        "--sort",
        action="append_const",
        const=Instruction.SORT,
        dest="instructions",
    )
    parser.add_argument(
        "--sort-reverse",
        action="append_const",
        const=Instruction.SORT_REVERSE,
        dest="instructions",
    )
    parser.set_defaults(instructions=[])
    kwargs = vars(parser.parse_args(args))
    try:
        run(*kwargs.pop("filepatterns"), **kwargs)
    except Exception:
        logging.exception("toml_sorted failed!")
        sys.exit(1)
