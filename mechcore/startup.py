#!/usr/bin/env python3

import os
import subprocess

from modules import motion_subsystem, weapons_subsystem, diagnostics_subsystem


def opener(path, flags):
    return os.open(path, flags, 0o666)


def main():
    os.umask(0)
    with open("/tmp/mode", "w", opener=opener) as f:
        f.write("IDLE")

    print("Starting up system")

    initialization_count = 0
    expected_initializations = 5
    success = motion_subsystem.initialize()
    if success:
        initialization_count += 1
        print('SUCCESS')
    else:
        print('FAILED')

    success = diagnostics_subsystem.initialize()
    if success:
        initialization_count += 1
        print('SUCCESS')
    else:
        print('FAILED')

    success = weapons_subsystem.initialize('gatling')
    if success:
        initialization_count += 1
        print('SUCCESS')
    else:
        print('FAILED')

    success = weapons_subsystem.initialize('laser')
    if success:
        initialization_count += 1
        print('SUCCESS')
    else:
        print('FAILED')

    success = weapons_subsystem.initialize('missiles')
    if success:
        initialization_count += 1
        print('SUCCESS')
    else:
        print('FAILED')

    if initialization_count == 0:
        print("NO COMPONENTS LOADED CORRECTLY")
    elif initialization_count < expected_initializations:
        print(f"LOADING FAILED FOR {expected_initializations - initialization_count} MODULES.")
    else:
        print("ALL COMPONENTS LOADED CORRECTLY")

    print("Waiting for MAINTENANCE MODE ..")

    with open("/tmp/mode", "r") as f:
        mode = f.read().strip()

    if mode == "COMBAT":
        print("No weapon system detected")
        print("Cannot initiate combat mode")
    elif mode == "IDLE":
        print("System in stand-by.")
        return
    elif mode == "MAINTENANCE":
        print("System in maintenance mode.")
        print("Waiting for command.")
        subprocess.call(["/bin/bash"])
    else:
        print("Unknown mode detected.")


if __name__ == "__main__":
    main()
