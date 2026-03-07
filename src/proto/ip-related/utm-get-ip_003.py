#!/usr/bin/env python3
import argparse
import subprocess
import plistlib
import re
from pathlib import Path


def get_vm_path(vm_name):
    """Parse `utmctl list` output to find the VM path."""
    result = subprocess.run(
        ["utmctl", "list"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        # Example line:
        # Ubuntu (Running) /Users/me/Library/Containers/.../Ubuntu.utm
        if vm_name in line:
            parts = line.split()
            for part in parts:
                if part.endswith(".utm"):
                    return Path(part)

    raise ValueError(f"VM '{vm_name}' not found in `utmctl list` output")


def get_mac_from_config(vm_path):
    """Extract MAC address from config.plist inside the .utm bundle."""
    config_path = vm_path / "config.plist"
    if not config_path.exists():
        raise RuntimeError(f"config.plist not found in {vm_path}")

    config = plistlib.loads(config_path.read_bytes())

    try:
        mac = config["NetworkDevices"][0]["MACAddress"]
        return mac.lower()
    except Exception:
        raise RuntimeError("Could not read MAC address from config.plist")


def find_ip_from_mac(mac):
    """Search ARP table and DHCP leases for the VM's IP."""
    mac_clean = mac.replace(":", "").lower()

    # 1. ARP table
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

    # 2. DHCP leases
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


def main():
    parser = argparse.ArgumentParser(
        description="Get the IP address of a running UTM VM"
    )
    parser.add_argument("vm_name", help="Name of the UTM virtual machine")
    args = parser.parse_args()

    vm_path = get_vm_path(args.vm_name)
    mac = get_mac_from_config(vm_path)
    ip = find_ip_from_mac(mac)

    if ip:
        print(ip)
    else:
        print("IP address not found")


if __name__ == "__main__":
    main()

