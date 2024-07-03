from transformers import pipeline
from mqtt import client, base_topic
import os

model = os.environ.get("TEXT_CLASSIFICATION_MODEL", "j-hartmann/emotion-english-distilroberta-base")
classifier = pipeline("text-classification", model=model, return_all_scores=True)
print(f"Using classifier model: {model}")

def commands_callback(model_output):
    print("")
    print("")
    print("----------------------------------------------------")
    print("")
    print("user said:")
    print(model_output)
    print("")
    classified = classifier(model_output)[0]

    print("feels like:")
    for sentiment in classified:
        print(f"{sentiment['label'].ljust(8)} {sentiment['score']}")

        # Send to MQTT
        try:
            print(f"Sending to MQTT: {base_topic}/{sentiment['label']}, {sentiment['score']}")
            client.publish(base_topic + "/" + sentiment['label'], sentiment['score'])
        except:
            print("Failed to send to MQTT")

    print("")
    print("----------------------------------------------------")
    print("")
    print("")
