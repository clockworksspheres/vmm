#!/usr/bin/env python3
import argparse
import subprocess
import plistlib
import re
from pathlib import Path


def get_vm_ip(vm_name):
    # 1. Query UTM for VM list (plist format)
    result = subprocess.run(
        ["utmctl", "list", "--format", "plist"],
        capture_output=True,
        text=False
    )
    plist = plistlib.loads(result.stdout.strip())

    # Find VM entry by name
    vm = next((v for v in plist if v["name"] == vm_name), None)
    if not vm:
        raise ValueError(f"VM '{vm_name}' not found")

    vm_path = Path(vm["path"])

    # 2. Read MAC address from config.plist
    config_path = vm_path / "config.plist"
    config = plistlib.loads(config_path.read_bytes())

    try:
        mac = config["NetworkDevices"][0]["MACAddress"].lower()
    except Exception:
        raise RuntimeError("Could not read MAC address from VM config")

    # Normalize MAC for matching
    mac_nocolon = mac.replace(":", "").lower()

    # 3. Scan ARP table
    try:
        arp_output = subprocess.check_output(["arp", "-a"], text=True)
        for line in arp_output.splitlines():
            m = re.search(r"\((.*?)\).*? at ([0-9a-f:]+)", line)
            if m:
                ip, mac_found = m.groups()
                if mac_found.replace(":", "").lower() == mac_nocolon:
                    return ip
    except Exception:
        pass

    # 4. Fallback: scan DHCP leases
    leases_file = Path("/var/db/dhcpd_leases")
    if leases_file.exists():
        leases = leases_file.read_text()
        m = re.search(
            r"ip_address=(.*?)\n.*?hw_address=1," + mac_nocolon,
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
    parser.add_argument(
        "vm_name",
        help="Name of the UTM virtual machine"
    )

    args = parser.parse_args()

    ip = get_vm_ip(args.vm_name)
    if ip:
        print(ip)
    else:
        print("IP address not found")


if __name__ == "__main__":
    main()

