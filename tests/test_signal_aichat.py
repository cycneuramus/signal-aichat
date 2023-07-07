import os
import sys
import unittest


class TestScriptImport(unittest.TestCase):
    def test_import_without_issues(self):
        try:
            sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

            import signal_aichat
            self.assertTrue(True)

        except ImportError as e:
            self.fail(f"Import error: {e}")


if __name__ == '__main__':
    unittest.main()
