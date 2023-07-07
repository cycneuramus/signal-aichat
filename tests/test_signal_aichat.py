import os
import sys
import unittest


class TestScriptImport(unittest.TestCase):
    def test_import_without_issues(self):
        """Test if script executes without import errors"""
        try:
            # Add the parent directory (where my_script.py resides) to the sys.path
            sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

            # Now Python should be able to import my_script
            import signal_aichat
            self.assertTrue(True)

        except ImportError as e:
            # If there was an ImportError, make the test fail.
            self.fail(f"Import error: {e}")


if __name__ == '__main__':
    unittest.main()
