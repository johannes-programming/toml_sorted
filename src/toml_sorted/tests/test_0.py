from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from toml_sorted.core import main, run, sorted_data


class TestSortedData(unittest.TestCase):
    def test_sorts_dict_keys(self) -> None:
        self.assertEqual(
            sorted_data(data={"z": 1, "a": 2, "m": 3}, reverse=False),
            {"a": 2, "m": 3, "z": 1},
        )

    def test_sorts_sequences(self) -> None:
        self.assertEqual(sorted_data(data=[3, 1, 2], reverse=False), [1, 2, 3])
        self.assertEqual(sorted_data(data=(3, 1, 2), reverse=True), (3, 2, 1))


class TestRun(unittest.TestCase):
    def test_sorts_top_level_keys_from_file_to_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            infile = root / "input.toml"
            outfile = root / "output.toml"
            infile.write_text("z = 3\na = 1\nm = 2\n", encoding="utf-8")

            run(infile=str(infile), outfile=str(outfile))

            self.assertEqual(
                outfile.read_text(encoding="utf-8"), "a = 1\nm = 2\nz = 3\n"
            )

    def test_reverse_sorts_top_level_keys_from_file_to_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            infile = root / "input.toml"
            outfile = root / "output.toml"
            infile.write_text("a = 1\nz = 3\nm = 2\n", encoding="utf-8")

            run(infile=str(infile), reverse=True, outfile=str(outfile))

            self.assertEqual(
                outfile.read_text(encoding="utf-8"), "z = 3\nm = 2\na = 1\n"
            )

    def test_sorts_selected_nested_list(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            infile = root / "input.toml"
            outfile = root / "output.toml"
            infile.write_text(
                "[tool.demo]\nvalues = [3, 1, 2]\n", encoding="utf-8"
            )

            run(
                infile=str(infile),
                keys=["tool", "demo", "values"],
                outfile=str(outfile),
            )

            self.assertEqual(
                outfile.read_text(encoding="utf-8"),
                "[tool.demo]\nvalues = [\n    1,\n    2,\n    3,\n]\n",
            )

    def test_reads_stdin_and_writes_stdout(self) -> None:
        stdout = io.StringIO()

        with (
            patch("builtins.input", return_value="z = 3\na = 1\n"),
            redirect_stdout(stdout),
        ):
            run()

        self.assertEqual(stdout.getvalue(), "a = 1\nz = 3\n")


class TestMain(unittest.TestCase):
    def test_main_accepts_cli_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            infile = root / "input.toml"
            outfile = root / "output.toml"
            infile.write_text("z = 3\na = 1\n", encoding="utf-8")

            main(["--infile", str(infile), "--outfile", str(outfile)])

            self.assertEqual(
                outfile.read_text(encoding="utf-8"), "a = 1\nz = 3\n"
            )

    def test_main_accepts_key_and_reverse_arguments(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            infile = root / "input.toml"
            outfile = root / "output.toml"
            infile.write_text(
                "[tool.demo]\nvalues = [1, 3, 2]\n", encoding="utf-8"
            )

            main(
                [
                    "--infile",
                    str(infile),
                    "--key",
                    "tool",
                    "--key",
                    "demo",
                    "--key",
                    "values",
                    "--reverse",
                    "--outfile",
                    str(outfile),
                ]
            )

            self.assertEqual(
                outfile.read_text(encoding="utf-8"),
                "[tool.demo]\nvalues = [\n    3,\n    2,\n    1,\n]\n",
            )


if __name__ == "__main__":
    unittest.main()
