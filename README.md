# Raspberry-Weather-DS18B20
=========================

**Forked from https://github.com/peterkodermac/Raspberry-Weather-DS18B20**

This python script uses two sensors and a Raspberry Pi to read temperature, humidity, as well as readings from 
[openweathermap.org](https://openweathermap.org/), and stores readings in Elasticsearch. 
For full write-up, visit [alonsoarteaga.me](https://alonsoarteaga.me).

#### Important env variables to set up
- ES_URL: location of elasticsearch. I.e: http://test.com[:portNum for ES, 9200]
- ES_INDEX: name of ES index. i.e: rpi_temps
- OW_API_KEY: api key for openweathermaps.org

TODOS:
- [x] Include outside weather temp and; add test.
- [x] __Fix dht22 sensor crash issue__ wiring error fixes
- [x] __Find better solution for cronjob env variables__ fixed by writing vars in /etc/environment
- [ ] Mock test api call to ES
- [ ] Set up docker 
- [ ] Set up CI/CD
- [ ] Set up automatic deployment to pi / git webhooks
- [ ] Write better documentation/ include sources I used
- [ ] Rewrite to golang
- [ ] Find weatherproof/outdoor assembly for the pi to sit outside
- [ ] Add a try/catch to check if OW_API_KEY is empty to skip this step if the value is empty
