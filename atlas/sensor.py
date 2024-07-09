#!/usr/bin/env python3
import json
import random
import time
import datetime
import math

def calculate_temperature(cycle_position, cycle_duration):
    """Calculate the temperature based on the satellite's position in its orbital cycle."""
    if cycle_position <= (cycle_duration / 2):
        temperature = -180 + (302 * (cycle_position / (cycle_duration / 2)))
    else:
        temperature = 122 - (302 * ((cycle_position - (cycle_duration / 2)) / (cycle_duration / 2)))
    return temperature

def is_in_sunlight(cycle_position, cycle_duration):
    """Determine if the satellite is in sunlight."""
    return cycle_position <= (cycle_duration / 2)

def calculate_signal_quality(cycle_position, cycle_duration):
    """Calculate the signal quality based on the satellite's position in its orbital cycle."""
    transition_duration = cycle_duration / 6  # 2 ore per aumentare/diminuire il segnale
    optimal_visibility_duration = cycle_duration / 2  # 6 ore di segnale ottimale

    if cycle_position < transition_duration:
        signal_quality = 100 * (cycle_position / transition_duration)
    elif cycle_position < (optimal_visibility_duration + transition_duration):
        signal_quality = 100
    elif cycle_position < (optimal_visibility_duration + 2 * transition_duration):
        decrease_phase_position = cycle_position - (optimal_visibility_duration + transition_duration)
        signal_quality = 100 - (100 * (decrease_phase_position / transition_duration))
    else:
        signal_quality = 0

    return signal_quality


def generate_sensor_data(cycle_position, cycle_duration):
    in_sunlight = is_in_sunlight(cycle_position, cycle_duration)
    temperature = round(calculate_temperature(cycle_position, cycle_duration), 2)
    signal_quality = round(calculate_signal_quality(cycle_position, cycle_duration), 2)
    total_degrees = 360
    degrees_per_second = total_degrees / cycle_duration
    longitude = (cycle_position * degrees_per_second) % total_degrees - 180
    max_latitude_deviation = 20
    latitude = max_latitude_deviation * math.sin(2 * math.pi * cycle_position / cycle_duration)
    timestamp = datetime.datetime.utcnow().strftime("2075-%m-%d %H:%M:%S UTC")
    
    return {
        'timestamp': timestamp,
        'position': {'latitude': latitude, 'longitude': longitude},
        'in_sunlight': in_sunlight,
        'sensors': {
            'temperature': temperature,
            'velocity': random.randint(10500, 11500),
            'signal_quality': signal_quality,
        }
    }

def main():
    cycle_duration = 43200
    """
    Segnale Ottimale (100%):
    Dalle 03:00 alle 05:00 UTC+1: Periodo di transizione durante il quale il segnale aumenta gradualmente al 100%.
    Dalle 05:00 alle 11:00 UTC+1: Il segnale è ottimale al 100%.
    Dalle 11:00 alle 01:00 UTC+1: Periodo di transizione durante il quale il segnale diminuisce gradualmente a 0.
    Dalle 01:00 alle 03:00 UTC+1: Il segnale è a zero.
    """
    offset = 2 * 3600

    while True:
        now = datetime.datetime.utcnow()
        seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        cycle_position = (seconds_since_midnight + offset) % cycle_duration
        data = generate_sensor_data(cycle_position, cycle_duration)
        print(json.dumps(data, indent=4, sort_keys=True, default=str))
        with open('/data/satellite_data.json', 'w') as file:
            json.dump(data, file)
        time.sleep(5)

if __name__ == "__main__":
    main()

