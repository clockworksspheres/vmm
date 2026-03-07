#!/usr/bin/env python3
import argparse
import subprocess
import re
from pathlib import Path


UTM_STATE_DIR = Path.home() / "Library/Containers/com.utmapp.UTM/Data/Library/State"


def get_vm_uuid(vm_name):
    """Parse `utmctl list` and return the UUID for the matching VM."""
    result = subprocess.run(
        ["utmctl", "list"],
        capture_output=True,
        text=True
    )

    lines = result.stdout.splitlines()

    for line in lines[1:]:  # skip header
        parts = line.split()
        if len(parts) < 3:
            continue

        uuid = parts[0]
        name = " ".join(parts[2:])

        if vm_name.lower() in name.lower():
            return uuid

    raise ValueError(f"VM '{vm_name}' not found.\nAvailable VMs:\n{result.stdout}")


def get_vm_ip_from_state(uuid):
    """Read QEMU runtime logs to extract the VM's IP address."""
    state_dir = UTM_STATE_DIR / uuid

    if not state_dir.exists():
        raise RuntimeError(f"No state directory found for UUID {uuid}")

    ifup_log = state_dir / "qemu-ifup.log"
    if not ifup_log.exists():
        raise RuntimeError("qemu-ifup.log not found (VM may not be running)")

    text = ifup_log.read_text()

    # Look for IPv4 address
    m = re.search(r"(\d+\.\d+\.\d+\.\d+)", text)
    if m:
        return m.group(1)

    return None


def main():
    parser = argparse.ArgumentParser(
        description="Get the IP address of a UTM VM (any version)"
    )
    parser.add_argument("vm_name", help="Name of the UTM virtual machine")
    args = parser.parse_args()

    uuid = get_vm_uuid(args.vm_name)
    ip = get_vm_ip_from_state(uuid)

    if ip:
        print(ip)
    else:
        print("IP address not found")


if __name__ == "__main__":
    main()

