#!/usr/bin/env python3
import wave
import numpy as np
import io
import morse3
from morse_audio_decoder.morse import MorseCode
import tempfile
import argparse
import paho.mqtt.client as mqtt
from threading import Thread
import time
import base64

REQUIREMENTS = """
paho-mqtt<2.0.0
morse-audio-decoder==0.1.1
morse3==2.9
"""

SHARED = {}

def wav_to_text(wf:bytearray) -> str:
    with tempfile.NamedTemporaryFile(mode="wb") as tf:
        tf.write(wf)
        tf.seek(0)
        morse_code_obj = MorseCode.from_wavfile(tf.name)
        decoded_morse_code = morse_code_obj.decode()
    return decoded_morse_code

def text_to_wav(text:str) -> io.BytesIO:
    morse = text_to_morse(text)
    return morse_to_wav(morse)

def text_to_morse(text:str) ->str:
    m = morse3.Morse(text)
    return m.stringToMorse()

def morse_to_text(morse:str) ->str:
    m = morse3.Morse(morse)
    return m.morseToString()

# Function to generate a sine wave for a given duration and frequency
def generate_sine_wave(frequency, duration, sample_rate=8000, amplitude=0.5):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

# Function to convert Morse code to a WAV file and return it as a bytes object
def morse_to_wav(morse_code):
    sample_rate = 8000  # 8 kHz sampling rate
    unit_duration = 0.1  # duration of one unit
    dot = generate_sine_wave(1000, unit_duration, sample_rate)
    dash = generate_sine_wave(1000, unit_duration * 3, sample_rate)
    silence_unit = np.zeros(int(sample_rate * unit_duration))
    silence_letter = np.zeros(int(sample_rate * unit_duration * 3))
    silence_word = np.zeros(int(sample_rate * unit_duration * 7))

    audio_sequence = []

    for symbol in morse_code:
        if symbol == '.':
            audio_sequence.extend(dot)
            audio_sequence.extend(silence_unit)
        elif symbol == '-':
            audio_sequence.extend(dash)
            audio_sequence.extend(silence_unit)
        elif symbol == ' ':
            audio_sequence.extend(silence_letter)
        elif symbol == '/':
            audio_sequence.extend(silence_word)

    audio_sequence = np.array(audio_sequence, dtype=np.float32)

    # Create an in-memory bytes buffer
    wav_buffer = io.BytesIO()

    # Save the audio sequence as a WAV file in the buffer
    wav_file = wave.open(wav_buffer, 'w')
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes((audio_sequence * 32767).astype(np.int16).tobytes())
    wav_file.close()

    # Reset buffer position to the beginning
    wav_buffer.seek(0)

    return wav_buffer

# Callback function when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(f"{SHARED['topic']}/read")

def on_message(client:mqtt.Client, userdata, msg):
    try:
        payload = base64.b64decode(msg.payload)
        tm = wav_to_text(payload)
        print("<", tm)
    except Exception as e:
        print("Exception", e)
        pass

# Subscriber function
def mqtt_subscriber():
    client:mqtt.Client = SHARED['client']
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(SHARED['host'], SHARED['port'], 60)
    client.loop_forever()

# Publisher function
def mqtt_publisher():
    client:mqtt.Client = SHARED['client']
    client.loop_start()

    print("Enter the message to publish (or 'exit' to quit):")
    while True:
        message = input(">")
        if message.lower() == 'exit':
            break
        wm = text_to_wav(message)
        with wm:
            wm.seek(0)
            b64 = base64.b64encode(wm.read())
        client.publish(f"{SHARED['topic']}/write", b64)

    client.loop_stop()
    client.disconnect()

# Main function
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mqtthost")
    parser.add_argument("mqttport", type=int)
    parser.add_argument("frequency", help="VLF ITU 4", type=int)
    args = parser.parse_args()
    client = mqtt.Client()

    SHARED.update({
        'client': client,
        'host': args.mqtthost,
        'port': args.mqttport,
        'topic': f"frequency/{args.frequency}"
    })

    t = Thread(target=mqtt_subscriber, daemon=True)
    t.start()
    while not client.is_connected():
        time.sleep(0.05)
    mqtt_publisher()

if __name__ == "__main__":
   main()
