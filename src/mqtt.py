import paho.mqtt.client as mqtt
import random
import os


# Settings
host = os.environ.get("MQTT_HOST", "test.mosquitto.org")
user = os.environ.get("MQTT_USER", None)
pwd = os.environ.get("MQTT_PWD", None)
clientID = os.environ.get("MQTT_CLIENT_ID", "mqtt_client_id") + "-" + str(random.randint(0, 1000))
base_topic = os.environ.get("MQTT_BASE_TOPIC", "sentiment_analysis_base_topic")

# Connect & start
client = mqtt.Client(clientID)
if(user and pwd):
    client.username_pw_set(user, pwd)
else:
    print("No user or password set for MQTT, trying connecting without credentials.")

client.will_set(base_topic)
client.connect(host)
client.loop_start()