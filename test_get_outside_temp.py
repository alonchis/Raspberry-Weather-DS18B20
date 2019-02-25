import unittest
from unittest import TestCase
from unittest.mock import patch

from getInfo import get_outside_temp

JSON_RESPONSE = "{\"main\": {\"humidity\": 93,\"pressure\": 1037,\"temp\": 75,\"temp_max\": 276.15,\"temp_min\": 271.15}, \"name\":\"Springfield\"}"

class TestGet_outside_temp(TestCase):
    @patch('getInfo.requests.get')
    def test_get_outside_temp(self, mock_get):
        mock_get.return_value.status_code = 200
        response = get_outside_temp()
        self.assertEqual(response.status_code, 200)

    @patch('getInfo.requests.get')
    def test_get_outside_temp_parse_json(self, mock_get):
        mock_get.get = "http://test.com"
        mock_get.return_value.ok = True
        mock_get.return_value.text = JSON_RESPONSE
        expected = {'city': 'Springfield', 'humidity':93, 'temp':75}

        actual = get_outside_temp()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    if __name__ == '__main__':
        unittest.main()
