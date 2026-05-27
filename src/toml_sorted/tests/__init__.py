import unittest

__all__ = ["test"]


def test() -> unittest.TextTestResult:
    loader: unittest.TestLoader
    tests: unittest.TestSuite
    loader = unittest.TestLoader()
    tests = loader.discover(start_dir="toml_sorted.tests")
    return unittest.TextTestRunner().run(tests)
