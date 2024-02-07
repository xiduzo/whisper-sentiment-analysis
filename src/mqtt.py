import paho.mqtt.client as mqtt
import random

# Settings
host="37.97.203.138"
user="mdduser"
pwd="IoTMDD"
clientID="talk-to-water" + str(random.randint(0, 1000))
base_topic="my_project"

# Connect & start
client = mqtt.Client(clientID)
client.username_pw_set(user, pwd)
client.will_set(base_topic)
client.connect(host)
client.loop_start()