#!/usr/bin/env python3

import os
import subprocess
import time

from modules import motion_subsystem, weapons_subsystem, diagnostics_subsystem


def opener(path, flags):
    return os.open(path, flags, 0o666)


def main():
    os.umask(0)
    with open("/tmp/mode", "w", opener=opener) as f:
        f.write("COMBAT")

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

    print("Starting warmachine mode ..")

    with open("/tmp/mode", "r") as f:
        mode = f.read().strip()

    if mode == "COMBAT":
        print("Initiated combat mode.")
        print("Enemy nearby detected.")
        print("Engaging combat.")
        subprocess.call("/usr/local/bin/killenemies")
    elif mode == "IDLE":
        print("System in stand-by.")
        while True:
            time.sleep(0.1)
    elif mode == "MAINTENANCE":
        print("System in maintenance mode.")
        print("Waiting for command.")
        subprocess.call(["/bin/bash"])
    else:
        print("Unknown mode detected.\nInitiating self destruction in 3.. 2.. 1..")
        subprocess.call("/usr/local/bin/killenemies")


if __name__ == "__main__":
    main()
