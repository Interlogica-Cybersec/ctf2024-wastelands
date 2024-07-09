#!/usr/bin/env python3
import socket
import threading
import time
import subprocess
from queue import Queue
import json

def get_signal_quality():
    data_path = "/data/satellite_data.json"
    try:
        with open(data_path, 'r') as file:
            data = json.load(file)
            return data['sensors']['signal_quality']
    except Exception as e:
        print(f"Error reading from {data_path}: {e}")
        return 0

allowed_commands = ["telemetry", "id", "date", "uname"]

def handle_uplink(conn, downlink_queue):

    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            try:
                command = data.decode('utf-8', errors='ignore').strip()
                print(f"Executing command (uplink): {command}")
                if command == 'glitch':
                    output = '''
Congratulations! You found an ADV Glitch! DV Cyber Security #1

We monitor and protect your company 24/7 with our SOC Services, ensuring uncompromised security.

Find out more on https://dvcybersecurity.it

DVCYBERSECURITY{5725bf04-40e1-409c-baab-8fd1e91653f6}
'''
                elif any(cmd for cmd in allowed_commands if command.startswith(cmd)):
                    signal_quality = get_signal_quality()
                    delay = (101 - signal_quality) / 4
                    time.sleep(delay)

                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                else:
                    output = "0"

            except subprocess.CalledProcessError as e:
                output = "0"
            except Exception as e:
                output = "0"

            downlink_queue.put(output)

        except Exception as e:
            print(f"An error occurred in handle_uplink: {e}")
            break

def handle_downlink(conn, downlink_queue):
    signal_quality = get_signal_quality()
    delay = (101 - signal_quality) / 4
    time.sleep(delay)

    telemetry_message = ""
    try:
        with open("/data/satellite_data.json", 'r') as file:
            telemetry_data = json.load(file)
            telemetry_message = "Timestamp: {}\n".format(telemetry_data['timestamp'])
            telemetry_message += "In Sunlight: {}\n".format("Yes" if telemetry_data['in_sunlight'] else "No")
            telemetry_message += "Latitude: {}°\n".format(telemetry_data['position']['latitude'])
            telemetry_message += "Longitude: {}°\n".format(telemetry_data['position']['longitude'])
            telemetry_message += "Sensors:\n"
            telemetry_message += "  Temperature: {}°C\n".format(telemetry_data['sensors']['temperature'])
            telemetry_message += "  Velocity: {} km/h\n".format(telemetry_data['sensors']['velocity'])
            telemetry_message += "  Signal Quality: {}%\n".format(telemetry_data['sensors']['signal_quality'])
    except Exception as e:
        print(f"Error reading telemetry data: {e}")
        telemetry_message = "Telemetry data unavailable due to error."

    conn.sendall(b'\nDWNLNK\n\n' + telemetry_message.encode() + b'\n')

    while True:
        if not downlink_queue.empty():
            command_output_message = downlink_queue.get()
            message = f"\n{command_output_message}\n"
            conn.sendall(message.encode())
        else:
            time.sleep(max(0.1, delay))


def start_server(port, handler):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(1)
    print(f"Server listening on port {port}")
    while True:
        conn, addr = server.accept()
        print(f"Connected to {addr}")
        threading.Thread(target=handler, args=(conn,)).start()

if __name__ == "__main__":
    downlink_queue = Queue()

    threading.Thread(target=start_server, args=(5000, lambda conn: handle_uplink(conn, downlink_queue))).start()
    threading.Thread(target=start_server, args=(5001, lambda conn: handle_downlink(conn, downlink_queue))).start()

