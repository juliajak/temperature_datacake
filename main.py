from mqtt import MQTTClient
import time
import ujson
import machine
import config
import pycom
from pycoproc import Pycoproc
from SI7006A20 import SI7006A20


def sub_cb(topic, msg):
   print(msg)

# MQTT Setup
client = MQTTClient(config.SERIAL_NUMBER,
                    config.MQTT_BROKER,
                    user=config.TOKEN,
                    password=config.TOKEN,
                    port=config.PORT)
client.set_callback(sub_cb)
client.connect()
print('connected to MQTT broker')

# The MQTT topic that we publish data to
my_topic = config.TOPIC

while True:
    py = Pycoproc()
    si = SI7006A20(py)
    temperature = str(si.temperature())
    client.publish(topic=my_topic, msg=str(temperature))
    client.check_msg()
    print("Send data to MQTT broker, sleeping for 15 minutes...")
    time.sleep(900) # Wait 15 minutes (900 seconds)
