#!/usr/bin/env python3

import argparse
import hashlib
import os.path
import subprocess
from enum import Enum

from modules import maintenance, diagnostics, remote_control, self_destruction, glitch


class Action(Enum):
    maintenance = 'maintenance'
    diagnostics = 'diagnostics'
    remote_control = 'remote_control'
    self_destruction = 'self_destruction'
    glitch = 'glitch'


    def __str__(self):
        return str(self.value)


def md5(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
        return hashlib.md5(data).hexdigest()


def validate_key_files_signature(key1, key2):
    with open(key1, 'rb') as f1, open(key2, 'rb') as f2:
        key1_data = f1.read()
        key2_data = f2.read()

    return (
            key1_data != key2_data
            and md5(key1) == md5(key2)
            and b"TNKK" in key1_data
            and b"TNKK" in key2_data
    )


def main():
    parser = argparse.ArgumentParser(description="Please provide the two key files for authentication to activate secret project TNK-020.")
    parser.add_argument("--key1", help="Path to key1 file", required=True)
    parser.add_argument("--key2", help="Path to key2 file", required=True)
    parser.add_argument("--action", help="Action", type=Action, choices=list(Action), required=True)
    args = parser.parse_args()

    if args.action == Action.glitch:
        glitch.execute()
        return
    if not os.path.isfile(args.key1):
        print(f"File {args.key1} read error. Possible reason: file does not exist, file is a directory, insufficient permissions")
        return
    if not os.path.isfile(args.key2):
        print(f"File {args.key2} read error. Possible reason: file does not exist, file is a directory, insufficient permissions")
        return
    if args.action == Action.maintenance and validate_key_files_signature(args.key1, args.key2):
        maintenance.execute()
        return
    if args.action == Action.diagnostics and validate_key_files_signature(args.key1, args.key2):
        diagnostics.execute()
        return
    if args.action == Action.remote_control and validate_key_files_signature(args.key1, args.key2):
        remote_control.execute()
        return
    if args.action == Action.self_destruction and validate_key_files_signature(args.key1, args.key2):
        self_destruction.execute()
        return

    print("ACTION NOT AUTHORIZED. INITIATING DEFENSIVE PROCEDURE\n")
    subprocess.call("/usr/local/bin/killenemies")


if __name__ == "__main__":
    main()
