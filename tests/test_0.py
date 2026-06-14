import tempfile
import tomllib
import unittest
from pathlib import Path
from typing import Self

import tomli_w

from toml_sorted.core.run import run
from toml_sorted.enum.Instruction import Instruction

__all__ = ["TestTomlSort"]


class TestTomlSort(unittest.TestCase):

    def test_run_sorts_matching_toml_file(self: Self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.toml"

            with path.open("wb") as stream:
                tomli_w.dump({"b": 2, "a": 1}, stream)

            run(
                str(path),
                instructions=[Instruction.SORT],
            )

            with path.open("rb") as stream:
                result = tomllib.load(stream)

        self.assertEqual(result, {"a": 1, "b": 2})

    def test_run_ignores_duplicate_glob_matches(self: Self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.toml"

            with path.open("wb") as stream:
                tomli_w.dump({"b": 2, "a": 1}, stream)

            run(
                str(path),
                str(path),
                instructions=[Instruction.SORT],
            )

            with path.open("rb") as stream:
                result = tomllib.load(stream)

        self.assertEqual(result, {"a": 1, "b": 2})


if __name__ == "__main__":
    unittest.main()
