# Raspberry-Weather-DS18B20
=========================

forked from https://github.com/peterkodermac/Raspberry-Weather-DS18B20
This code helps you read temperatures along with humidity and save both in your database. You need to configure your weather station in order to use this code. Read more on www.raspberryweather.com

#### Purpose:
wanted to setup a weather station on a raspberry pi using the sensors DS18B20 (weatherproof probe) and a DHT22 (moisture and temperature probe, non waterproof). The problem I found was that the DS18B20 probe is read from a file in /something/devices/28-0000000/w1-slave, and the DHT22 readings come from a python script. im sure there is a way to read DHT22 from a file just like the other probe but this is what worked from me. I found another python script somewhere else (TODO: citation needed) som by frankensteining these two scripts, I managed to make this work. 

A difference in this project from Kodermac's is that im sending the readings to an elastic stack, instead of mysql/wordpress. why? because at the time, im working on an ELK project and i wanted some more experience. 

As of now I'm keeping the Pi/sensors in my room until I find an weatherproof solution to put it outside. why include it? because I thought it would be neat to compare the inside/outside temperatures. 

Also, I think I figured out the DHT22 sensor issue: the sensor is actually calles AM3202 (which contains a DHT22 sensor inside). main difference is housing and included resistors. I followed wiring instructions for DHT22 and the sensor crashed after a while. Now I've rewired following the AM3202 instructions and it seems to work. will monitor for uptime...

#### How to run:
A couple things would need to be changed in the python script: 
- Change the elasticsearch host ip
- Set up a cron job. I tested every minute to start collecting documents in ES by setting the cron job (crontab -e) to * * * * * {{path to project directory}}/getInfo.py. in the future i plan on changing this to maybe every 5 minutes?
  - NOTE: I've since discovered the pains of running python scripts as cron jobs. the issue is that i had sourced env variables in a file on my home dir, and running the script would run whenever i manually ran it. cron is a different user and runs under a different environment. I hotfixed this by including the env variables on the cron job i.e: * * * * * ES_INDEX="some_index" ES_URL="some url" python3 /path/to/script	

#### Important env variables to set up
- ES_URL: location of elasticsearch. I.e: http://test.com[:portNum for ES, 9200]
- ES_INDEX: name of ES index. i.e: rpi_temps
- OW_API_KEY: api key for openweathermaps.org

TODOS:
- [x] include outside weather temp and; add test;
- [ ] fix dht22 sensor crash issue (fixed)?
- [ ] find better solution for cronjob env variables
- [ ] mock test api call to ES
- [ ] set up docker 
- [ ] set up CI/CD
- [ ] set up automatic deployment to pi / git webhook
- [ ] write better documentation/ include sources i used
- [ ] rewrite to golang
- [ ] find weatherproof/outdoor assembly for the pi to sit outside
- [ ] add a try/catch to check if OW_API_KEY is empty to skip this step if the value is empty
