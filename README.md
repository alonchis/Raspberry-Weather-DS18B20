Raspberry-Weather-DS18B20
=========================

forked from https://github.com/peterkodermac/Raspberry-Weather-DS18B20
This code helps you read temperatures along with humidity and save both in your database. You need to configure your weather station in order to use this code. Read more on www.raspberryweather.com

purpose: wanted to setup a weather station on a raspberry pi using the sensors DS18B20 (weatherproof probe) and a DHT22 (moisture and temperature probe, non waterproof). The problem I found was that the DS18B20 probe is read from a file in /something/devices/28-0000000/w1-slave, and the DHT22 readings come from a python script. im sure there is a way to read DHT22 from a file just like the other probe but this is what worked from me. I found another python script somewhere else (TODO: citation needed) som by frankensteining these two scripts, I managed to make this work. 

A difference in this project from Kodermac's is that im sending the readings to an elastic stack, instead of mysql/wordpress. why? because at the time, im working on an ELK project and i wanted some more experience. 


how to run:
a couple things would need to be changed in the python script. 
	* change the elasticsearch host ip
	* set up a cron job. i tested every minute to start collecting documents in ES by setting the cron job (crontab -e) to * * * * * {{path to project directory}}/getInfo.py. in the future i plan on changing this to maybe every 5 minutes?
	
