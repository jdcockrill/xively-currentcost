#!/usr/bin/python

import logging
import logging.config
import xively
import serial
import re
import traceback
import sys
import datetime
import os

API_KEY=os.environ['API_KEY']
FEED_ID=os.environ['FEED_ID']

T_STREAM="temperature_sensor"
W_STREAM="electricity_sensor"

temp_pat=re.compile(r"<tmpr>\d{1,2}\.\d")
watt_pat=re.compile(r"<watts>\d{5}")

def get_datastream(feed, stream):
  try:
    datastream = feed.datastreams.get(stream)
    print "Found existing stream:", stream
    return datastream
  except:
    print "Stream not found:", stream
    raise

class StreamHandler:
  def __init__(self):
    self.streams = {}

  def set_stream(self, name, dstream):
    self.streams[name] = dstream

  def update_stream(self, name, value):
    self.streams[name].current_value = value
    self.streams[name].at = datetime.datetime.utcnow()
    self.streams[name].update()

def get_streamhandler(feed, temp_stream, watt_stream):
  temp_dstream = get_datastream(feed, temp_stream)
  watt_dstream = get_datastream(feed, watt_stream)

  temp_dstream.max_value = None
  temp_dstream.min_value = None
  watt_dstream.max_value = None
  watt_dstream.min_value = None
  
  handler = StreamHandler()
  handler.set_stream('temp', temp_dstream)
  handler.set_stream('watt', watt_dstream)

  return handler
 
def run(sr, handler):
  logger = logging.getLogger("xively")
  logger.info("Starting")
  count=-1
  try:
    while True:
      # read a line from the serial port
      line = sr.readline()
      # make sure it's well-formed, otherwise bin it
      if line.startswith('<msg>'):
        # take 1 in every 5 readings (should be 1 every 30 seconds)
        count += 1
        if count % 5 == 0:
          try:
            # extract the values
            temp=float(temp_pat.search(line).group(0)[6:])
            watts=int(watt_pat.search(line).group(0)[7:])
            logger.debug("temp: " + str(temp))
            logger.debug("watt: " + str(watts))
            # send the data
            handler.update_stream('temp', temp)
            handler.update_stream('watt', watts)
            logger.debug("updates posted to xively")
          except AttributeError:
            pass
  except KeyboardInterrupt as ki:
    pass
  except Exception as e:
    logger.exception("Exception caught")
  finally:
    logger.info("exiting")
    sr.close()

def main():
  # Setup the serial port
  sr=serial.Serial('/dev/ttyAMA0', 57600)
  sr.open()
  # Setup the Xively feed and streams
  api = xively.XivelyAPIClient(API_KEY)
  feed = api.feeds.get(FEED_ID)

  handler = get_streamhandler(feed, T_STREAM, W_STREAM)

  run(sr, handler)

if __name__ == "__main__":
  logging.config.fileConfig(CONFIG_DIR + '/logging.conf')
  rlogger = logging.getLogger('root')
  rlogger.info("cc_xively started")
  main()

# test data (should probably make a unit test with this)
#<msg><src>CC128-v0.11</src><dsb>01075</dsb><time>09:33:50</time><tmpr>17.8</tmpr><sensor>0</sensor><id>03595</id><type>1</type><ch1><watts>00440</watts></ch1></msg>

