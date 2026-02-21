#!/usr/bin/env python3
"""
vmx.py - Multi-hypervisor CLI wrapper: VMware (vmrun), VirtualBox (VBoxManage), UTM (utmctl)

Runs on macOS to support VMware Fusion, VirtualBox and UTM.

Supports: list, start, stop, suspend, reset, snapshot, snapshots, status, ip
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Tuple

# Adjust paths if needed
VMRUN = "/Applications/VMware Fusion.app/Contents/Library/vmrun"
VBOXMANAGE = "VBoxManage"
UTMCTL = "utmctl"  # e.g. /Applications/UTM.app/Contents/MacOS/utmctl

def run(cmd: list, check=True, capture_output=False, text=True, shell=False):
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=capture_output,
            text=text,
            encoding="utf-8" if text else None,
            shell=shell
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd) if not shell else cmd}", file=sys.stderr)
        if e.stderr:
            print(e.stderr.strip(), file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Command not found: {cmd[0] if not shell else 'shell command'}", file=sys.stderr)
        sys.exit(1)


def detect_hypervisor_and_clean_vm(vm_str: str) -> Tuple[str, str]:
    vm = vm_str.strip()

    if vm.lower().startswith("vmware:"):
        return "vmware", vm[7:].strip()
    if vm.lower().startswith("virtualbox:"):
        return "virtualbox", vm[11:].strip()
    if vm.lower().startswith("utm:"):
        return "utm", vm[4:].strip()

    p = Path(vm)
    if p.suffix.lower() == ".vmx" or "vmwarevm" in p.name.lower():
        return "vmware", vm
    if p.suffix.lower() in (".vbox", ".vdi"):
        return "virtualbox", vm

    return "utm", vm


def list_vms():
    print("=== VMware VMs ===")
    run([VMRUN, "list"], capture_output=False)

    print("\n=== VirtualBox VMs ===")
    run([VBOXMANAGE, "list", "vms"], capture_output=False)

    print("\n=== UTM VMs ===")
    try:
        run([UTMCTL, "list"], capture_output=False)
    except SystemExit:
        print("(utmctl not available — macOS/UTM only?)")


def start_vm(hyper: str, vm: str, headless: bool = True):
    if hyper == "vmware":
        args = [VMRUN, "-T", "fusion", "start", vm, "nogui" if headless else "gui"]
        run(args)
    elif hyper == "virtualbox":
        args = [VBOXMANAGE, "startvm", vm]
        if headless:
            args += ["--type", "headless"]
        run(args)
    elif hyper == "utm":
        run([UTMCTL, "start", vm])
    else:
        sys.exit(f"Unknown hypervisor: {hyper}")


def stop_vm(hyper: str, vm: str):
    if hyper == "vmware":
        run([VMRUN, "stop", vm, "soft"])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "controlvm", vm, "acpipowerbutton"])
    elif hyper == "utm":
        run([UTMCTL, "stop", vm])
    else:
        sys.exit(f"Unknown hypervisor: {hyper}")


def suspend_vm(hyper: str, vm: str):
    if hyper == "vmware":
        run([VMRUN, "suspend", vm, "soft"])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "controlvm", vm, "savestate"])
    elif hyper == "utm":
        print("Note: UTM uses 'pause' → use 'start' to resume.")
        run([UTMCTL, "pause", vm])
    else:
        sys.exit(f"Suspend not supported for {hyper}")


def reset_vm(hyper: str, vm: str, hard: bool = False):
    if hyper == "vmware":
        power_type = "hard" if hard else "soft"
        run([VMRUN, "reset", vm, power_type])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "controlvm", vm, "reset"])
    elif hyper == "utm":
        print("UTM: Using restart (force stop + start)")
        run([UTMCTL, "stop", vm])
        run([UTMCTL, "start", vm])
    else:
        sys.exit(f"Reset not supported for {hyper}")


def create_snapshot(hyper: str, vm: str, snapshot_name: str):
    if hyper == "vmware":
        run([VMRUN, "snapshot", vm, snapshot_name])
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "snapshot", vm, "take", snapshot_name])
    elif hyper == "utm":
        print("Warning: utmctl does not natively support snapshots.")
        print("→ Use qcow2 images + manual QEMU tools or UTM GUI.")
        sys.exit(1)
    else:
        sys.exit(f"Snapshots not supported for {hyper}")


def list_snapshots(hyper: str, vm: str):
    if hyper == "vmware":
        run([VMRUN, "listSnapshots", vm, "showtree"], capture_output=False)
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "snapshot", vm, "list", "--details"], capture_output=False)
    elif hyper == "utm":
        print("UTM does not support listing snapshots via utmctl.")
        print("→ Check UTM GUI or qcow2 internals manually.")
    else:
        sys.exit(f"Snapshots not supported for {hyper}")


def status_vm(hyper: str, vm: str):
    if hyper == "vmware":
        run([VMRUN, "list"], capture_output=False)
        print(f"\nFor '{vm}':")
        run([VMRUN, "getGuestIPAddress", vm, "-wait"], check=False)
    elif hyper == "virtualbox":
        run([VBOXMANAGE, "showvminfo", vm], capture_output=False)
    elif hyper == "utm":
        run([UTMCTL, "status", vm])
    else:
        sys.exit(f"Unknown hypervisor: {hyper}")


def get_ip(hyper: str, vm: str):
    if hyper == "vmware":
        run([VMRUN, "getGuestIPAddress", vm, "-wait"])
    elif hyper == "virtualbox":
        run([
            VBOXMANAGE, "guestproperty", "get", vm,
            "/VirtualBox/GuestInfo/Net/0/IP"
        ])
    elif hyper == "utm":
        run([UTMCTL, "ip-address", vm])
    else:
        sys.exit(f"IP query not supported for {hyper}")


def main():
    parser = argparse.ArgumentParser(
        description="Multi-hypervisor VM control (VMware / VirtualBox / UTM)",
        epilog="VM identifiers: path/to/vm.vmx | vmware:name | virtualbox:name | utm:name | just name (defaults to UTM)"
    )
    #subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers = parser.add_subparsers(dest="command")

    # list
    p_list = subparsers.add_parser(
        "list",
        help="List all VMs across hypervisors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  vmx.py list
  vmx.py list                  # shows VMware, VirtualBox, and UTM VMs
"""
    )

    # start
    p_start = subparsers.add_parser(
        "start",
        help="Start a VM (headless by default)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  vmx.py start utm:MyUbuntu
  vmx.py start virtualbox:Win11 --no-headless
  vmx.py start vmware:/path/to/MyVM/My.vmx
"""
    )
    p_start.add_argument("vm", help="VM identifier")
    p_start.add_argument("--no-headless", action="store_true", help="Start with GUI (if supported)")

    # stop
    p_stop = subparsers.add_parser(
        "stop",
        help="Gracefully stop a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  vmx.py stop utm:MyUbuntu
  vmx.py stop virtualbox:DebianTest
"""
    )
    p_stop.add_argument("vm", help="VM identifier")

    # suspend
    p_suspend = subparsers.add_parser(
        "suspend",
        help="Suspend / save state of a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  vmx.py suspend vmware:MyLinux
  vmx.py suspend virtualbox:WinTest
  # Note: UTM uses 'pause' (resume with 'start')
"""
    )
    p_suspend.add_argument("vm", help="VM identifier")

    # reset
    p_reset = subparsers.add_parser(
        "reset",
        help="Reset / reboot a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  vmx.py reset vmware:MyServer
  vmx.py reset virtualbox:Win11 --hard         # force reset
  vmx.py reset utm:DevBox                      # stop + start
"""
    )
    p_reset.add_argument("vm", help="VM identifier")
    p_reset.add_argument("--hard", action="store_true", help="Hard/force reset (where supported)")

    # snapshot
    p_snapshot = subparsers.add_parser(
        "snapshot",
        help="Create a new snapshot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  vmx.py snapshot vmware:MyVM "Before update"
  vmx.py snapshot virtualbox:Debian "Clean install state"
  # UTM: not natively supported via utmctl
"""
    )
    p_snapshot.add_argument("vm", help="VM identifier")
    p_snapshot.add_argument("name", help="Snapshot name (quote if it contains spaces)")

    # snapshots (alias: list-snapshots)
    p_snapshots = subparsers.add_parser(
        "snapshots",
        help="List snapshots for a VM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  vmx.py snapshots vmware:/path/to/MyVM/My.vmx
  vmx.py snapshots virtualbox:Production
  # UTM: not supported via utmctl
"""
    )
    p_snapshots.add_argument("vm", help="VM identifier")

    # status
    p_status = subparsers.add_parser(
        "status",
        help="Show VM status / running state",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  vmx.py status utm:MyLinuxVM
  vmx.py status vmware:TestServer
"""
    )
    p_status.add_argument("vm", help="VM identifier")

    # ip
    p_ip = subparsers.add_parser(
        "ip",
        help="Get guest IP address (requires guest tools)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  vmx.py ip vmware:/Users/roy/VMs/Ubuntu/Ubuntu.vmx
  vmx.py ip virtualbox:Win10
  vmx.py ip utm:DevBox
"""
    )
    p_ip.add_argument("vm", help="VM identifier")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "list":
        list_vms()
        return

    hyper, clean_vm = detect_hypervisor_and_clean_vm(args.vm)

    if not clean_vm:
        parser.error("No VM specified")

    cmd = args.command

    if cmd == "start":
        start_vm(hyper, clean_vm, headless=not args.no_headless)
        print(f"Started {hyper}:{clean_vm}")

    elif cmd == "stop":
        stop_vm(hyper, clean_vm)
        print(f"Stopped {hyper}:{clean_vm}")

    elif cmd == "suspend":
        suspend_vm(hyper, clean_vm)
        print(f"Suspended {hyper}:{clean_vm}")

    elif cmd == "reset":
        reset_vm(hyper, clean_vm, hard=args.hard)
        print(f"Reset {hyper}:{clean_vm} ({'hard' if args.hard else 'soft'})")

    elif cmd == "snapshot":
        create_snapshot(hyper, clean_vm, args.name)
        print(f"Created snapshot '{args.name}' for {hyper}:{clean_vm}")

    elif cmd in ("snapshots", "list-snapshots"):
        list_snapshots(hyper, clean_vm)

    elif cmd == "status":
        status_vm(hyper, clean_vm)

    elif cmd == "ip":
        get_ip(hyper, clean_vm)


if __name__ == "__main__":
    main()


