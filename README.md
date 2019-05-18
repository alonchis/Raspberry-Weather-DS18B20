# Raspberry-Weather-DS18B20
=========================

forked from https://github.com/peterkodermac/Raspberry-Weather-DS18B20
This code helps you read temperatures along with humidity and save both in your database. You need to configure your weather station in order to use this code. Read more on www.raspberryweather.com

#### Purpose:
I wanted to setup a weather station on a raspberry pi using the sensors DS18B20 (weatherproof probe) and a DHT22 (moisture and temperature probe, non waterproof). The problem I found was that the DS18B20 probe readings come from a file in /sys/bus/devices/28-0000000/w1-slave, and the DHT22 readings come from a python script. im sure there is a way to read DHT22 from a file too , or viceversa, but this is what worked from me. I found another python script somewhere else (TODO: citation needed) so I frankenstein'd these two scripts and it works! 

Why not just follow Kodermac's excellent write up on making this work?
The main difference in this project from Kodermac's is that im sending the readings to an elastic stack, whereas Kodermac uses  mysql/wordpress to store/view the results. 
But why elasticsearch? because at the time, I was working on an ELK project and I wanted some more experience with it. 

As of now I'm keeping the Pi/sensors in my room until I find an weatherproof solution to put it outside, so the script also fetches temperature from openweather.org. Until I figure out a permanent outdoor solution, the script sends both temps to elasticsearch.

Also, I've found a weird bug with the DHT22 sensor where it would stop recording after a while: the sensor is actually called AM3202 (which contains a DHT22 sensor inside). main difference is housing and included resistors. I followed wiring instructions for DHT22 and the sensor crashed after a while. Now I've rewired following the AM3202 instructions and it seems to work. will monitor for uptime...

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
