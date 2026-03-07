#!/usr/bin/env python3
import argparse
import plistlib
from pathlib import Path

def detect_os_from_config(config):
    """Detect OS from UTM config.plist."""
    system = config.get("System", {})
    os_type = system.get("OperatingSystem")
    if os_type:
        return os_type

    # Infer from drives
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

    return "Unknown"


def inspect_vm(utm_path: Path):
    """Inspect a single .utm VM bundle."""
    config_path = utm_path / "config.plist"

    if not config_path.exists():
        return (utm_path.name, "Invalid (no config.plist)")

    try:
        with open(config_path, "rb") as f:
            config = plistlib.load(f)
    except Exception as e:
        return (utm_path.name, f"Error reading config: {e}")

    os_type = detect_os_from_config(config)
    return (utm_path.name, os_type)


def main():
    parser = argparse.ArgumentParser(
        description="Detect OS type (macOS/Linux/Windows) of UTM VMs."
    )
    parser.add_argument(
        "path",
        help="Path to a .utm VM or a directory containing multiple .utm VMs"
    )
    args = parser.parse_args()

    target = Path(args.path)

    if not target.exists():
        print("Path does not exist.")
        return

    # Single VM
    if target.is_dir() and target.suffix == ".utm":
        name, os_type = inspect_vm(target)
        print(f"{name}: {os_type}")
        return

    # Directory of VMs
    if target.is_dir():
        utm_vms = list(target.glob("*.utm"))
        if not utm_vms:
            print("No .utm VMs found in directory.")
            return

        for vm in utm_vms:
            name, os_type = inspect_vm(vm)
            print(f"{name}: {os_type}")
        return

    print("Provided path is not a .utm bundle or directory.")


if __name__ == "__main__":
    main()

