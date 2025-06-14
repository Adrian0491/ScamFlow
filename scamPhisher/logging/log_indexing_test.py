import unittest

from unittest.mock import patch
from log_indexing import *

class TestLogging(unittest.TestCase):
    def setUp(self):
        self.logger = Logging(log_dir="logs/test")

    @patch('logging.Logger.info')
    def test_info_log(self, mock_info):
        msg = "Test info"
        result = self.logger.info(msg)

        mock_info.assert_called_once_with(msg)
        self.assertIn("[INFO]", result)
        self.assertIn(msg, result)

    @patch('logging.Logger.warning')
    def test_warning_log(self, mock_warning):
        msg = "Test warning"
        result = self.logger.warning(msg)

        mock_warning.assert_called_once_with(msg)
        self.assertIn("[WARNING]", result)
        self.assertIn(msg, result)

    @patch('logging.Logger.error')
    def test_error_log(self, mock_error):
        msg = "Test error"
        result = self.logger.error(msg)

        mock_error.assert_called_once_with(msg)
        self.assertIn("[ERROR]", result)
        self.assertIn(msg, result)

if __name__ == '__main__':
    unittest.main()
