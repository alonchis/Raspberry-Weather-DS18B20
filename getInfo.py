import os
import glob
import sys
import re
import time
import subprocess
#import MySQLdb as mdb
import datetime
import sched
import Adafruit_DHT
import requests
import elasticsearch
import decimal
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

es = elasticsearch.Elasticsearch(['alonsoarteaga.com:9200'])
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
sensor = 22
pin = 4

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
temperature = temperature * 9.0  / 5.0 + 32

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
def get_readings_dht22():
  if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
    result = "humidity = {}, temperature = {}".format(humidity, temperature)
    return result
  else:
    print('Failed to get reading. Try again!')
    sys.exit(1)


def read_temp_raw():
    catdata = subprocess.Popen(['cat',device_file],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
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
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
                #return temp_c
        return temp_f


read_temp_results = read_temp()
print(datetime.datetime.now().isoformat())
print("waterproof sensor reads ", read_temp_results)
print("DHT22 temp = ", temperature, " humidity = ", humidity)
API_ENDPOINT = "http://192.168.0.105:9200"
ES_INDEX = "rpi-temp"
es.index(index=ES_INDEX, doc_type='sensors', body={
    '@timestamp': datetime.datetime.now(),
    'temp probe temp': read_temp_results,
    'DHT22 temp': temperature,
    'DHT22 humidity': humidity
})
