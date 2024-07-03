import paho.mqtt.client as mqtt
import random
import os


# Settings
host = os.environ.get("MQTT_HOST", "test.mosquitto.org")
user = os.environ.get("MQTT_USER", None)
pwd = os.environ.get("MQTT_PWD", None)
clientID = os.environ.get("MQTT_CLIENT_ID", "mqtt_client_id") + "-" + str(random.randint(0, 1000))
base_topic = os.environ.get("MQTT_BASE_TOPIC", "sentiment_analysis_base_topic")

print(f"Using MQTT host: {host}")
print(f"Using MQTT user: {user}")
print(f"Using MQTT password: {pwd}")
print(f"Using MQTT clientID: {clientID}")
print(f"Using MQTT base_topic: {base_topic}")

# Connect & start
try:
    client = mqtt.Client(clientID)
except:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, clientID)

if(user and pwd):
    client.username_pw_set(user, pwd)
else:
    print("No user or password set for MQTT, trying connecting without credentials.")

def on_connect(client, userdata, flags, rc):
    if rc==0:
      print(">>>>>>> MQTT connected")
    else:
      print("Bad connection Returned code=",rc)

client.will_set(base_topic)
client.connect(host)
client.on_connect = on_connect
client.loop_start()
