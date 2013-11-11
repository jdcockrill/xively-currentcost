#Xively CurrentCost
I had a CurrentCost energy monitor, a Raspberry Pi and an old Cosm (now Xively) account kicking around, so I thought I'd put them to good use. I started with a Raspberry Pi but in time I'd like to switch it for an Arduino and use the Pi as a central station for relaying data from a number of sensors, perhaps.


##Python

Everything is in the python sub-directory. This script requires the following Python libraries:
- pyserial
- xively-python
- PyYaml

If you install this script using ```setup.py``` You need to set ```API_KEY``` and ```FEED_ID``` as environment variables for the script to pick them up. The ```cc_xively.py``` script expects to find these in ```/etc/xively-currentcost/xively.conf```. An example config file is created as part of the ```setup.py install``` process.

Lastly, you will probably work this out, but it expects there to be two channels/datastreams on your Xively feed. These should be named:
- ```electricity_sensor```; and
- ```temperature sensor```

There is an init.d script that is installed automatically as part of ```setup.py install```, so you should be able to start it with ```sudo service cc_xively start``` and check the logs in ```/var/log/xively.log```

###Final notes
If you want it to automatically start on boot, run the following once you've run the Python install:

```bash
sudo update-rc.d cc_xively defaults
```

I also have a CC128 model monitor, which uses pin 4 for GND and pin 8 for the TX part of the Serial communications. This is what you want to feed into the 'RX' pin on your Raspberry Pi.

##Arduino

To-do.
