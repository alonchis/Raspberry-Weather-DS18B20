import datetime
import glob
import json
import os
import subprocess
import sys
import time
import Adafruit_DHT
import elasticsearch
import requests
import contants

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

ES_INDEX = os.environ['ES_INDEX']
es = elasticsearch.Elasticsearch([os.environ['ES_URL']])

ds18b20_base_dir = '/sys/bus/w1/devices/'
ds18b20_device_folder = glob.glob(ds18b20_base_dir + '28*')[0]
ds18b20_device_file = ds18b20_device_folder + '/w1_slave'

OPENWEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather?id=4893811&APPID=' + os.environ['OW_API_KEY'] + '&units=imperial'

# todo extract to function, write unit test
# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(22, 26)

# Un-comment the line below to convert the temperature to Fahrenheit.
try:
    temperature = temperature * 9.0 / 5.0 + 32
except Exception:
    temperature = -273.15


def get_outside_temp():
    resp = requests.get(OPENWEATHER_URL)
    if resp.ok:
        response = json.loads(resp.text)
        result = {'city': response['name'], 'humidity': response['main']['humidity'], 'temp': response['main']['temp']}
        return result
    else:
        return None

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
def get_readings_dht22():
    if humidity is not None and temperature is not None:
        print('DHT22 readings: Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        result = "humidity = {}, temperature = {}".format(humidity, temperature)
        return result
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)


def read_temp_raw():
    catdata = subprocess.Popen(['cat', ds18b20_device_file],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        # return temp_c
        return temp_f


def build_and_send_payload(dht22_temp, dht22_humid, DS18B20_readings):
    result = es.index(index=ES_INDEX, doc_type='sensors', body={
        '@timestamp': datetime.datetime.utcnow(),
        'temp probe temp': DS18B20_readings,
        'DHT22 temp': dht22_temp,
        'DHT22 humidity': dht22_humid,
        'outside temp': get_outside_temp()
    })
    return result


read_temp_results = read_temp()
print(datetime.datetime.now().isoformat())
print("waterproof sensor reads ", read_temp_results)
print("DHT22 temp = ", temperature, " humidity = ", humidity)
print(build_and_send_payload(temperature, humidity, read_temp_results))
