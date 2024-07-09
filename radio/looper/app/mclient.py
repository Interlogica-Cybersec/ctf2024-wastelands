#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
from threading import Thread
from morseclient import text_to_wav, wav_to_text
import base64

# Define the MQTT broker details
BROKER_ADDRESS = "mqtt"
#Very low frequency	VLF	4	3–30 kHz 100–10 km https://en.wikipedia.org/wiki/Radio_spectrum
TOPIC_CLIENT = "frequency/1337"
TOPIC_SPAM = "frequency/3137"
FREQ_RECV = 28497
TOPIC_RECV = f"frequency/{FREQ_RECV}"
FREQ_FLAG = 24148
TOPIC_FLAG = f"frequency/{FREQ_FLAG}"
FLAG = "FLAG NTRLGC L0LM0RS315M3553DUP"
SURVIVED = "I HAVE SURVIVED"
#TEST123 EXPLODES LOL

# Callback function when the client connects to the broker
def on_connect(client:mqtt.Client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(f"{TOPIC_RECV}/write")
    client.subscribe(f"{TOPIC_FLAG}/write")

# Callback function when a message is received from the broker
def on_message(client:mqtt.Client, userdata, msg):
    password = "TEST123"
    try:
        payload = base64.b64decode(msg.payload)
        tm = wav_to_text(payload)
        print(f"Message received: {msg.topic} {tm}")
        if msg.topic == f"{TOPIC_RECV}/write":
            if tm == SURVIVED:
                messages = [
                    "HI SURVIVOR",
                    "IF YOU ARE READING THIS",
                    "I AM DEAD",
                    "IF YOU NEED CAR COMPONENTS",
                    "CHECK THE GARAGE",
                    "TO GET THE CODE",
                    "SEND THE FOLLOWING",
                    f"PASSWORD TO {FREQ_FLAG}",
                    password
                ]
                message = ' '.join(messages)
                wf = text_to_wav(message)
                with wf:
                    b64 = base64.b64encode(wf.read())
                client.publish(f"{TOPIC_RECV}/read", b64)
        elif msg.topic == f"{TOPIC_FLAG}/write":
            print("PASSWORD CHECK")
            if tm == password:
                print("PASSWORD CONFIRMED!")
                wf = text_to_wav(FLAG)
                with wf:
                    b64 = base64.b64encode(wf.read())
                client.publish(f"{TOPIC_FLAG}/read", b64)

    except Exception as e:
        print("Exception", msg.topic, e)
        pass

# Publisher function
def mqtt_publisher():
    client = mqtt.Client()
    client.connect(BROKER_ADDRESS, 1883, 60)
    client.loop_start()

    with open('morseclient.py','rb') as mc:
        pyclient = base64.b64encode(mc.read())

    message = f"SEND {SURVIVED} TO {FREQ_RECV}"
    with text_to_wav(message) as wf:
        b64 = base64.b64encode(wf.read())
    
    # key = SURVIVED
    # with text_to_wav(key) as kf:
    #     kw = kf.read()
    # client.publish(TOPIC_RECV, kw)
    # time.sleep(10)
    # key = "TEST123 test"
    # with text_to_wav(key) as kf:
    #     kw = kf.read()
    # client.publish(TOPIC_FLAG, kw)

    while True:
        time.sleep(10)
        client.publish(f"{TOPIC_CLIENT}/read", pyclient)
        client.publish(f"{TOPIC_SPAM}/read", b64)

# Subscriber function
def mqtt_subscriber():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, 1883, 60)
    client.loop_forever()

# Main function
def main():
    t = Thread(target=mqtt_publisher, daemon=True)
    t.start()
    mqtt_subscriber()

if __name__ == "__main__":
    main()
