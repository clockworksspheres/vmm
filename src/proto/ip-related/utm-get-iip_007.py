#!/usr/bin/env python3
import plistlib
from pathlib import Path
import subprocess
import re

def safe_get(obj, key):
    if isinstance(obj, dict):
        return obj.get(key)
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict) and key in item:
                return item[key]
    return None

def get_vm_mac(utm_path):
    config_path = Path(utm_path) / "config.plist"
    config = plistlib.load(open(config_path, "rb"))
    net = config.get("Network", {})
    return safe_get(net, "MACAddress")

def find_ip_from_mac(mac):
    if not mac:
        return None

    mac = mac.lower()
    output = subprocess.check_output(["arp", "-a"]).decode()

    for line in output.splitlines():
        if mac in line.lower():
            match = re.search(r"\((.*?)\)", line)
            if match:
                return match.group(1)
    return None

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Find UTM VM IP from host")
    parser.add_argument("path", help="Path to .utm VM")
    args = parser.parse_args()

    mac = get_vm_mac(args.path)
    if not mac:
        print("Could not find MAC address in config.plist")
        return

    ip = find_ip_from_mac(mac)
    print("VM IP:", ip or "Not found (VM may be using SLIRP or not reachable)")

if __name__ == "__main__":
    main()

