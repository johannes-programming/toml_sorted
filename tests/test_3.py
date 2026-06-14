import io
import tempfile
import tomllib
import unittest
from pathlib import Path
from typing import Any, Self

import tomli_w

from toml_sorted.core.main import main

__all__ = ["TestCliAllIndices"]


class TestCliAllIndices(unittest.TestCase):
    def test_cli_accepts_all_indices_selector(self: Self) -> None:
        data: dict[str, Any]
        dataA: dict[str, Any]
        listA: list[str]
        path: Path
        stream: io.BufferedWriter
        tmpdir: str
        dataA = {
            "items": [
                {"b": 2, "a": 1},
                {"d": 4, "c": 3},
            ]
        }
        listA = [
            "--sort",
            "--key",
            "items",
            "--all-indices",
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "example.toml"
            with path.open("wb") as stream:
                tomli_w.dump(dataA, stream)
            main(listA + [str(path)])
            with path.open("rb") as stream:
                data = tomllib.load(stream)
        self.assertEqual(list(data["items"][0].keys()), ["a", "b"])
        self.assertEqual(list(data["items"][1].keys()), ["c", "d"])


if __name__ == "__main__":
    unittest.main()
