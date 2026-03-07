#!/usr/bin/env python3
import argparse
import plistlib
from pathlib import Path
import subprocess
import re


def safe_get(obj, key, default=None):
    """Safely extract a key from a dict or list of dicts."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict) and key in item:
                return item[key]
    return default


def detect_os_from_config(config):
    """Detect OS from UTM config.plist."""
    system = config.get("System", {})
    os_type = system.get("OperatingSystem")
    if os_type:
        return os_type

    drives = config.get("Drives", [])
    for drive in drives:
        path = drive.get("Path", "").lower()

        if path.endswith(".ipsw") or "macos" in path:
            return "macOS"

        if "win" in path or "windows" in path:
            return "Windows"

        if any(distro in path for distro in [
            "ubuntu", "fedora", "arch", "debian", "linux"
        ]):
            return "Linux"

    display = config.get("Display", {})
    network = config.get("Network", {})
    architecture = system.get("Architecture", "").lower()

    display_type = safe_get(display, "Type")
    network_device = safe_get(network, "Device")

    if system.get("Hypervisor") == "Apple":
        return "macOS"

    if system.get("TPMEnabled") is True:
        return "Windows"

    if display_type == "Spice" and network_device == "virtio-net":
        return "Linux"

    if architecture in ("aarch64", "arm64"):
        return "Linux"

    return "Unknown"


def get_vm_mac(config):
    """Extract MAC address from config."""
    net = config.get("Network", {})
    return safe_get(net, "MACAddress")


def find_ip_from_mac(mac):
    """Search ARP table for matching MAC."""
    if not mac:
        return None

    mac = mac.lower()
    try:
        output = subprocess.check_output(["arp", "-a"]).decode()
    except Exception:
        return None

    for line in output.splitlines():
        if mac in line.lower():
            match = re.search(r"\((.*?)\)", line)
            if match:
                return match.group(1)
    return None


def inspect_vm(utm_path: Path):
    """Return VM name, OS, MAC, and IP."""
    config_path = utm_path / "config.plist"

    if not config_path.exists():
        return (utm_path.name, "Invalid", None, None)

    try:
        with open(config_path, "rb") as f:
            config = plistlib.load(f)
    except Exception:
        return (utm_path.name, "Error", None, None)

    os_type = detect_os_from_config(config)
    mac = get_vm_mac(config)
    ip = find_ip_from_mac(mac)

    return (utm_path.name, os_type, mac, ip)


def main():
    parser = argparse.ArgumentParser(
        description="List all UTM VMs and their IP addresses."
    )
    parser.add_argument(
        "path",
        help="Directory containing .utm VMs"
    )
    args = parser.parse_args()

    target = Path(args.path)

    if not target.exists() or not target.is_dir():
        print("Path must be a directory containing .utm bundles.")
        return

    utm_vms = list(target.glob("*.utm"))
    if not utm_vms:
        print("No .utm VMs found.")
        return

    print(f"{'VM Name':20} {'OS':10} {'MAC Address':20} {'IP Address'}")
    print("-" * 70)

    for vm in utm_vms:
        name, os_type, mac, ip = inspect_vm(vm)
        print(f"{name:20} {os_type:10} {str(mac):20} {ip or 'N/A'}")


if __name__ == "__main__":
    main()

