#!/usr/bin/env python3
import subprocess
import socket
import json
import sys
import time

class Satellite:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def resolve_ip(name):
        try:
            return socket.gethostbyname(name)
        except socket.gaierror:
            print(f"Failed to resolve {name}.")
            return "Unresolved"

    def send_telemetry(self):
        time.sleep(1)
        print(f"{self.name}: Telemetry data transmission...")
        try:
            result = subprocess.run(["telemetry"], capture_output=True, text=True, check=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")

    @staticmethod
    def read_coordinates():
        try:
            with open('/data/satellite_data.json', 'r') as file:
                data = json.load(file)
                position = data.get('position', {})
                print(f"Position: Lat {position.get('latitude', 'Unknown')}, Long {position.get('longitude', 'Unknown')}")
        except FileNotFoundError:
            print("satellite_data.json not found.")

    def broadcast_coordinates(self):
        time.sleep(1)
        print(f"{self.name}: Broadcasting coordinates...")
        try:
            result = subprocess.run(["broadcast"], capture_output=True, text=True, check=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {e}")

def main():
    print("\nUsage: network.py [resolve|telemetry|coordinates|broadcast]\n")
    if len(sys.argv) < 2:
        print("Usage: network.py [resolve|telemetry|coordinates|broadcast]")
        sys.exit(1)

    satellite = Satellite("atlas01")
    action = sys.argv[1]

    if action == "resolve":
        if len(sys.argv) != 3:
            print("Usage: network.py resolve <satellite-name>")
        else:
            ip = Satellite.resolve_ip(sys.argv[2])
            print(f"Resolved IP: {ip}")
    elif action == "telemetry":
        satellite.send_telemetry()
    elif action == "coordinates":
        satellite.read_coordinates()
    elif action == "broadcast":
        satellite.broadcast_coordinates()
    else:
        print("Invalid action. Available actions: resolve, telemetry, coordinates, broadcast")
if __name__ == "__main__":
    main()
