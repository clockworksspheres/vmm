#!/usr/bin/env python3
import argparse
import subprocess
import plistlib
import re
from pathlib import Path
import os


UTM_DIR = Path.home() / "Library/Containers/com.utmapp.UTM/Data/Documents"


# ------------------------------------------------------------
# 1. Parse VM name from `utmctl list` table
# ------------------------------------------------------------
def get_vm_name_exact(user_input):
    result = subprocess.run(
        ["utmctl", "list"],
        capture_output=True,
        text=True
    )

    lines = result.stdout.splitlines()

    # Skip header
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 3:
            continue

        uuid = parts[0]
        status = parts[1]
        name = " ".join(parts[2:])  # VM names may contain spaces

        if user_input.lower() in name.lower():
            return name

    raise ValueError(
        f"VM '{user_input}' not found.\nAvailable VMs:\n{result.stdout}"
    )


# ------------------------------------------------------------
# 2. Find the .utm bundle by VM name
# ------------------------------------------------------------
def find_utm_bundle(vm_name):
    for entry in UTM_DIR.iterdir():
        if entry.name.lower().startswith(vm_name.lower()) and entry.suffix == ".utm":
            return entry
    raise RuntimeError(f"No .utm bundle found for VM '{vm_name}' in {UTM_DIR}")


# ------------------------------------------------------------
# 3. Extract MAC address from config.plist
# ------------------------------------------------------------
def get_mac_from_config(vm_path):
    config_path = vm_path / "config.plist"
    if not config_path.exists():
        raise RuntimeError(f"config.plist not found in {vm_path}")

    config = plistlib.loads(config_path.read_bytes())

    try:
        mac = config["NetworkDevices"][0]["MACAddress"]
        return mac.lower()
    except Exception:
        raise RuntimeError("Could not read MAC address from config.plist")


# ------------------------------------------------------------
# 4. Find IP address by matching MAC in ARP + DHCP leases
# ------------------------------------------------------------
def find_ip_from_mac(mac):
    mac_clean = mac.replace(":", "").lower()

    # --- ARP table ---
    try:
        arp_output = subprocess.check_output(["arp", "-a"], text=True)
        for line in arp_output.splitlines():
            m = re.search(r"\((.*?)\).*? at ([0-9a-f:]+)", line)
            if m:
                ip, mac_found = m.groups()
                if mac_found.replace(":", "").lower() == mac_clean:
                    return ip
    except Exception:
        pass

    # --- DHCP leases ---
    leases_file = Path("/var/db/dhcpd_leases")
    if leases_file.exists():
        leases = leases_file.read_text()
        m = re.search(
            r"ip_address=(.*?)\n.*?hw_address=1," + mac_clean,
            leases,
            re.S
        )
        if m:
            return m.group(1)

    return None


# ------------------------------------------------------------
# 5. Main CLI entry point
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Get the IP address of a running UTM VM"
    )
    parser.add_argument("vm_name", help="Name of the UTM virtual machine")
    args = parser.parse_args()

    vm_name = get_vm_name_exact(args.vm_name)
    vm_path = find_utm_bundle(vm_name)
    mac = get_mac_from_config(vm_path)
    ip = find_ip_from_mac(mac)

    if ip:
        print(ip)
    else:
        print("IP address not found")


if __name__ == "__main__":
    main()

