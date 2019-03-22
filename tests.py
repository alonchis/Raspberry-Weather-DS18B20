import re
from unittest.mock import patch

import getInfo

def test_get_readings_dht22_expect_success():
    actual = getInfo.get_readings_dht22()
    # pattern means a number between 0-9 (one or more)
    pattern = re.compile("humidity = [0-9]+.[0-9]+, temperature = [0-9]+.[0-9]+")
    result = bool(pattern.match(actual))
    assert result == True


def test_read_temp_raw_expect_not_null():
    actual = getInfo.read_temp_raw()
    assert len(actual) != 0

@patch('getInfo.Adafruit_DHT.read_retry')
def test_adafruit_read_retry(mock_get):
    mock_get.return_value.read_retry = 75.0, 30.0
    pass
